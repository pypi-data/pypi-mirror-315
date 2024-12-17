from megatron.core import tensor_parallel
from .mlp import MLP, MLPSubmodules
from megatron.core.transformer.module import MegatronModule
from megatron.core.transformer.spec_utils import ModuleSpec, build_module
from megatron.core.transformer.transformer_config import TransformerConfig


class MultimodalProjector(MegatronModule):
 
    def __init__(
        self,
        config: TransformerConfig,
        submodules: MLPSubmodules,
        projector_type: str,
        input_size: int,
    ):
        super().__init__(config=config)
        self.projector_type = projector_type

        assert submodules is not None, "MLPSubmodules must be provided"

        if self.projector_type == "mlp":
            self.encoder = MLP(config=config, submodules=submodules, input_size=input_size)
            self._encoder_key = 'encoder'
        elif self.projector_type == "affine":
            self.encoder = build_module(
                submodules.linear_fc1,
                input_size,
                config.hidden_size,
                config=config,
                init_method=config.init_method,
                gather_output=True,
                bias=config.add_bias_linear,
                skip_bias_add=True,
                is_expert=False,
                tp_comm_buffer_name=None,
            )
        else:
            raise Exception(f"Unsupported multimodal projection type {self.projector_type}")

    def forward(self, hidden_states):
        # Run encoder.
        encoder_output, encoder_output_bias = self.encoder(hidden_states)

        if encoder_output_bias is not None:
            encoder_output = encoder_output + encoder_output_bias

        return encoder_output
    
    #TODO 待确认
    def state_dict_for_save_checkpoint(self, prefix='', keep_vars=False):
        """For easy load."""
        state_dict_ = {}
        state_dict_[self._encoder_key] = self.encoder.state_dict_for_save_checkpoint(prefix=prefix, keep_vars=keep_vars)
        return state_dict_
    
     #TODO 待确认
    def load_state_dict(self, state_dict, strict=True):
        """For easy load."""
        self.encoder.load_state_dict(state_dict[self._encoder_key], strict=strict)