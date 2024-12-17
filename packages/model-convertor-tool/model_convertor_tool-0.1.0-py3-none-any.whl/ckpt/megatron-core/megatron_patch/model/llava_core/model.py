# Copyright (c) 2024 Alibaba PAI and Nvidia Megatron-LM Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Dict, Literal, Optional, Tuple, Union

import torch
from torch import Tensor

from megatron.core import InferenceParams, parallel_state, tensor_parallel
from megatron.core.dist_checkpointing.mapping import ShardedStateDict
from megatron.core.models.common.embeddings.language_model_embedding import LanguageModelEmbedding
from megatron.core.models.common.embeddings.rotary_pos_embedding import RotaryEmbedding
from megatron.core.models.common.language_module.language_module import LanguageModule
from megatron.core.packed_seq_params import PackedSeqParams
from megatron.core.transformer.enums import AttnMaskType, ModelType
from megatron.core.transformer.spec_utils import ModuleSpec
from megatron.core.utils import make_tp_sharded_tensor_for_checkpoint
from megatron.core.transformer.transformer_config import TransformerConfig

from .transformer_block import TransformerBlock

from megatron.training.arguments import core_transformer_config_from_args
from copy import deepcopy
from .config import get_vision_projection_config
from .layer_specs_llava import get_mlp_module_spec
from .multimodal_projector import MultimodalProjector
from megatron.training import get_args


class GPTModel(LanguageModule):
    """GPT Transformer language model.

    Args:
        config (TransformerConfig): Transformer config
        transformer_layer_spec (ModuleSpec): Specifies module to use for transformer layers
        vocab_size (int): Vocabulary size
        max_sequence_length (int): maximum size of sequence. This is used for positional embedding
        pre_process (bool, optional): Include embedding layer (used with pipeline parallelism). Defaults to True.
        post_process (bool, optional): Include an output layer (used with pipeline parallelism). Defaults to True.
        fp16_lm_cross_entropy (bool, optional): Defaults to False.
        parallel_output (bool, optional): Do not gather the outputs, keep them split across tensor parallel ranks. Defaults to True.
        share_embeddings_and_output_weights (bool, optional): When True, input embeddings and output logit weights are shared. Defaults to False.
        position_embedding_type (Literal[learned_absolute,rope], optional):  Position embedding type.. Defaults to 'learned_absolute'.
        rotary_percent (float, optional): Percent of rotary dimension to use for rotary position embeddings. Ignored unless position_embedding_type is 'rope'. Defaults to 1.0.
        rotary_base (int, optional): Base period for rotary position embeddings. Ignored unless position_embedding_type is 'rope'. Defaults to 10000.
        seq_len_interpolation_factor (Optional[float], optional): scale of linearly interpolating RoPE for longer sequences. The value must be a float larger than 1.0. Defaults to None.
    """

    def __init__(
        self,
        config: TransformerConfig,
        transformer_layer_spec: ModuleSpec,
        vocab_size: int,
        max_sequence_length: int,
        pre_process: bool = True,
        post_process: bool = True,
        fp16_lm_cross_entropy: bool = False,
        parallel_output: bool = True,
        share_embeddings_and_output_weights: bool = False,
        position_embedding_type: Literal['learned_absolute', 'rope'] = 'learned_absolute',
        rotary_percent: float = 1.0,
        rotary_base: int = 10000,
        seq_len_interpolation_factor: Optional[float] = None,
    ) -> None:
        super().__init__(config=config)

        self.transformer_layer_spec: ModuleSpec = transformer_layer_spec
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        self.pre_process = pre_process
        self.post_process = post_process
        self.fp16_lm_cross_entropy = fp16_lm_cross_entropy
        self.parallel_output = parallel_output
        self.share_embeddings_and_output_weights = share_embeddings_and_output_weights
        self.position_embedding_type = position_embedding_type

        # ==============================================================================
        self.args = get_args()
        self.untie_embeddings_and_output_weights = self.args.untie_embeddings_and_output_weights

        # 添加视觉编码器模块
        from .clip_encoder import CLIPVisionTower
        self.vision_tower = CLIPVisionTower(self.args.vision_tower)
        self.vision_tower.to(torch.half if self.args.fp16 else torch.bfloat16)

        # 冻结视觉编码器参数
        if self.args.freeze_clip_vision_tower:
            for param in self.vision_tower.parameters():
                param.requires_grad = False
        self.args.mm_hidden_size = self.vision_tower.hidden_size

        base_config = core_transformer_config_from_args(get_args())
        vision_projection_config = deepcopy(base_config)
        vision_projection_config = get_vision_projection_config(vision_projection_config, config.hidden_size)
        vision_projection_layer_spec = get_mlp_module_spec(use_te=True).submodules

        # 添加 projection 模块
        self.mm_projector = MultimodalProjector(
            vision_projection_config,
            vision_projection_layer_spec,
            "mlp",
            self.args.mm_hidden_size,)
        self._mm_projector_key ='mm_projector'
        self.mm_projector.to(torch.half if self.args.fp16 else torch.bfloat16)
        # ==============================================================================

        # megatron core pipelining currently depends on model type
        # TODO: remove this dependency ?
        self.model_type = ModelType.encoder_or_decoder

        # These 2 attributes are needed for TensorRT-LLM export.
        self.max_position_embeddings = max_sequence_length
        self.rotary_percent = rotary_percent

        if self.pre_process:
            self.embedding = LanguageModelEmbedding(
                config=self.config,
                vocab_size=self.vocab_size,
                max_sequence_length=self.max_sequence_length,
                position_embedding_type=position_embedding_type,
            )
            # 冻结语言模型 embeddings 参数
            if self.args.freeze_llm:
                for param in self.embedding.parameters():
                    param.requires_grad = False

        if self.position_embedding_type == 'rope':
            self.rotary_pos_emb = RotaryEmbedding(
                kv_channels=self.config.kv_channels,
                rotary_percent=rotary_percent,
                rotary_interleaved=self.config.rotary_interleaved,
                seq_len_interpolation_factor=seq_len_interpolation_factor,
                rotary_base=rotary_base,
            )

        # Transformer.
        self.decoder = TransformerBlock(
            config=self.config,
            spec=transformer_layer_spec,
            pre_process=self.pre_process,
            post_process=self.post_process,
        )
        # 冻结语言模型 decoder 参数
        if self.args.freeze_llm:
            for param in self.decoder.parameters():
                param.requires_grad = False

        # Output
        if post_process:
            if self.config.defer_embedding_wgrad_compute:
                # The embedding activation buffer preserves a reference to the input activations
                # of the final embedding projection layer GEMM. It will hold the activations for
                # all the micro-batches of a global batch for the last pipeline stage. Once we are
                # done with all the back props for all the microbatches for the last pipeline stage,
                # it will be in the pipeline flush stage. During this pipeline flush we use the
                # input activations stored in embedding activation buffer and gradient outputs stored
                # in gradient buffer to calculate the weight gradients for the embedding final linear layer.
                self.embedding_activation_buffer = []
                self.grad_output_buffer = []
            else:
                self.embedding_activation_buffer = None
                self.grad_output_buffer = None

            self.output_layer = tensor_parallel.ColumnParallelLinear(
                config.hidden_size,
                self.vocab_size,
                config=config,
                init_method=config.init_method,
                bias=False,
                skip_bias_add=False,
                gather_output=not self.parallel_output,
                skip_weight_param_allocation=self.pre_process
                and self.share_embeddings_and_output_weights,
                embedding_activation_buffer=self.embedding_activation_buffer,
                grad_output_buffer=self.grad_output_buffer,
            )
            # 冻结语言模型 output layer 参数
            if self.args.freeze_llm:
                for param in self.output_layer.parameters():
                    param.requires_grad = False

        if self.pre_process or self.post_process:
            self.setup_embeddings_and_output_layer()

    def set_input_tensor(self, input_tensor: Tensor) -> None:
        """Sets input tensor to the model.

        See megatron.model.transformer.set_input_tensor()

        Args:
            input_tensor (Tensor): Sets the input tensor for the model.
        """
        # This is usually handled in schedules.py but some inference code still
        # gives us non-lists or None
        if not isinstance(input_tensor, list):
            input_tensor = [input_tensor]

        assert len(input_tensor) == 1, 'input_tensor should only be length 1 for gpt/bert'
        self.decoder.set_input_tensor(input_tensor[0])

    def encode_images(self, images):
        image_features = self.vision_tower(images)
        image_features = self.mm_projector(image_features)
        return image_features

    def forward(
        self,
        input_ids: Tensor,
        position_ids: Tensor,
        attention_mask: Tensor,
        decoder_input: Tensor = None,
        labels: Tensor = None,
        inference_params: InferenceParams = None,
        packed_seq_params: PackedSeqParams = None,
        extra_block_kwargs: dict = None,
        tokentype_ids=None, # TODO
        images=None # TODO
    ) -> Tensor:
        """Forward function of the GPT Model This function passes the input tensors
        through the embedding layer, and then the decoeder and finally into the post
        processing layer (optional).

        It either returns the Loss values if labels are given  or the final hidden units
        """
        # If decoder_input is provided (not None), then input_ids and position_ids are ignored.
        # Otherwise, apply embedding layer on input_ids and position_ids to get decoder_input.

        # ==============================================================================
        if decoder_input is not None:
            pass
        elif self.pre_process:
            image_features = self.encode_images(images) # 576 * 4096

            input_embeds = self.embedding(input_ids, position_ids,
                                            tokentype_ids=tokentype_ids)
            input_embeds = input_embeds.permute(1, 0, 2)

            new_input_embeds = []
            from megatron_patch.data.llava.constants import IMAGE_TOKEN_INDEX
            for batch_idx, cur_input_ids in enumerate(input_ids):
                cur_input_embeds = input_embeds[batch_idx]  # s h
                if (cur_input_ids == IMAGE_TOKEN_INDEX).sum() == 0:
                    half_len = cur_input_ids.shape[0] // 2
                    cur_image_features = image_features[batch_idx]
                    cur_input_embeds_1 = cur_input_embeds[:half_len].unsqueeze(1)
                    cur_input_embeds_2 = cur_input_embeds[half_len:].unsqueeze(1)
                    cur_input_embeds = torch.cat([cur_input_embeds_1, cur_image_features[0:0], cur_input_embeds_2], dim=0)
                    new_input_embeds.append(cur_input_embeds)
                    continue
                image_token_indices = torch.where(cur_input_ids == IMAGE_TOKEN_INDEX)[0]
                cur_new_input_embeds = []
                cur_start = 0
                while image_token_indices.numel() > 0:
                    cur_image_features = image_features[batch_idx].unsqueeze(1)
                    image_token_start = image_token_indices[0]
                    if getattr(self.args, 'tune_mm_mlp_adapter', False) and getattr(self.args, 'mm_use_im_start_end', False):
                        cur_new_input_embeds.append(cur_input_embeds[cur_start:image_token_start-1].unsqueeze(1).detach())
                        cur_new_input_embeds.append(cur_input_embeds[image_token_start-1:image_token_start].unsqueeze(1))
                        cur_new_input_embeds.append(cur_image_features)
                        cur_new_input_embeds.append(cur_input_embeds[image_token_start+1:image_token_start+2].unsqueeze(1))
                        cur_start = image_token_start + 2
                    else:
                        cur_new_input_embeds.append(cur_input_embeds[cur_start:image_token_start].unsqueeze(1))
                        cur_new_input_embeds.append(cur_image_features)
                        cur_start = image_token_start + 1

                    image_token_indices = torch.where(cur_input_ids[cur_start:] == IMAGE_TOKEN_INDEX)[0]
                if cur_input_ids[cur_start:].numel() > 0:
                    if getattr(self.args, 'tune_mm_mlp_adapter', False) and getattr(self.args, 'mm_use_im_start_end', False):
                        cur_new_input_embeds.append(cur_input_embeds[cur_start:].unsqueeze(1).detach())
                    else:
                        cur_new_input_embeds.append(cur_input_embeds[cur_start:].unsqueeze(1))

                cur_new_input_embeds = [x.to(device=input_ids.device) for x in cur_new_input_embeds]
                cur_new_input_embeds = torch.cat(cur_new_input_embeds, dim=0)
                new_input_embeds.append(cur_new_input_embeds)

            decoder_input = torch.cat(new_input_embeds, dim=1)
            
            if attention_mask is not None:
                batch_size = input_ids.shape[0]
                from .modeling_attn_mask_utils import _prepare_4d_causal_attention_mask
                new_enc_attn_mask = _prepare_4d_causal_attention_mask(
                    attention_mask,
                    (batch_size, decoder_input.shape[0]),
                    decoder_input,
                    0
                )

            attention_mask = new_enc_attn_mask
        else:
            # intermediate stage of pipeline
            decoder_input = None
        # ==============================================================================

        # # Decoder embedding.
        # if decoder_input is not None:
        #     pass
        # elif self.pre_process:
        #     decoder_input = self.embedding(input_ids=input_ids, position_ids=position_ids)
        # else:
        #     # intermediate stage of pipeline
        #     # decoder will get hidden_states from encoder.input_tensor
        #     decoder_input = None

        # Rotary positional embeddings (embedding is None for PP intermediate devices)
        rotary_pos_emb = None
        if self.position_embedding_type == 'rope':
            rotary_seq_len = self.rotary_pos_emb.get_rotary_seq_len(
                inference_params, self.decoder, decoder_input, self.config
            )
            rotary_pos_emb = self.rotary_pos_emb(rotary_seq_len)

        # Run decoder.
        hidden_states = self.decoder(
            hidden_states=decoder_input,
            attention_mask=attention_mask,
            inference_params=inference_params,
            rotary_pos_emb=rotary_pos_emb,
            packed_seq_params=packed_seq_params,
            **(extra_block_kwargs or {}),
        )

        if not self.post_process:
            return hidden_states

        # logits and loss
        output_weight = None
        if self.share_embeddings_and_output_weights:
            output_weight = self.shared_embedding_or_output_weight()
        logits, _ = self.output_layer(hidden_states, weight=output_weight)

        if labels is None:
            # [s b h] => [b s h]
            return logits.transpose(0, 1).contiguous()

        loss = self.compute_language_model_loss(labels, logits)

        return loss

    def sharded_state_dict(
        self, prefix: str = '', sharded_offsets: tuple = (), metadata: Optional[Dict] = None
    ) -> ShardedStateDict:
        """ Sharded state dict implementation for GPTModel backward-compatibility (removing extra state).

        Args:
            prefix (str): Module name prefix.
            sharded_offsets (tuple): PP related offsets, expected to be empty at this module level.
            metadata (Optional[Dict]): metadata controlling sharded state dict creation.

        Returns:
            ShardedStateDict: sharded state dict for the GPTModel
        """
        sharded_state_dict = super().sharded_state_dict(prefix, sharded_offsets, metadata)
        output_layer_extra_state_key = f'{prefix}output_layer._extra_state'

        # Old GPT checkpoints only stored the output layer weight key. So we remove the _extra_state key
        # but check that it doesn't contain any data anyway
        output_extra_state = sharded_state_dict.pop(output_layer_extra_state_key, None)
        assert not (
            output_extra_state and output_extra_state.data
        ), f'Expected output layer extra state to be empty, got: {output_extra_state}'

        return sharded_state_dict


    # TODO
    # def state_dict_for_save_checkpoint(self, prefix='', keep_vars=False):
    #     """For easy load."""

    #     state_dict_ = {}
    #     #TODO 待确认
    #     # 将 mm_projector 保存
    #     state_dict_[self._mm_projector_key] \
    #         = self.mm_projector.state_dict_for_save_checkpoint(prefix=prefix, keep_vars=keep_vars)

    #     state_dict_["embedding"] \
    #         = self.embedding.state_dict_for_save_checkpoint(prefix=prefix, keep_vars=keep_vars)

    #     state_dict_["output_layer"] \
    #         = self.output_layer.state_dict(prefix=prefix, keep_vars=keep_vars)

    #     state_dict_["decoder"] \
    #         = self.decoder.state_dict_for_save_checkpoint(prefix=prefix, keep_vars=keep_vars)

    #     return state_dict_

    # def load_state_dict(self, state_dict, strict=True):
    #     """Customized load."""
    #     args = get_args()
    #     state_dict = state_dict["language_model"]
    #     #TODO
    #     # Load mm_projector.
    #     if self._mm_projector_key in state_dict:
    #         state_dict_ = state_dict[self._mm_projector_key]
    #         self.mm_projector.load_state_dict(state_dict_, strict=strict)

    #     self.decoder.load_state_dict(state_dict["encoder"], strict=strict)

    #     # Embedding.
    #     if self.pre_process:
    #         if "embedding" in state_dict:
    #             state_dict_ = state_dict["embedding"]
    #         self.embedding.load_state_dict(state_dict_, strict=strict)



    #     if self.post_process:
    #         if self.untie_embeddings_and_output_weights:
    #             assert 'output_layer' in state_dict, \
    #                 'could not find data for output_layer in the checkpoint'
    #             self.output_layer.load_state_dict(state_dict["output_layer"],
    #                                               strict=strict)

       