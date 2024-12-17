import os
import json
import torch
from collections import defaultdict
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
)

from transformers.modeling_utils import WEIGHTS_INDEX_NAME, WEIGHTS_NAME, shard_checkpoint, load_sharded_checkpoint
from megatron.training.initialize import initialize_megatron
from megatron.training import get_args
from megatron.training.checkpointing import get_checkpoint_name, get_checkpoint_tracker_filename, read_metadata

import sys
path_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.join(path_dir, "examples"))
from qwen_core.pretrain_mcore_qwen import model_provider
from megatron_patch.arguments import get_patch_args

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

import debugpy

# try:
#     print("Starting debugpy...")
#     debugpy.listen(("localhost", 10000))
#     print("Waiting for debugger attach")
#     debugpy.wait_for_client()
# except Exception as e:
#     print("debug 失败")

def add_model_args(parser):

    parser.add_argument(
        "--target-tensor-model-parallel-size",
        type=int,
        default=1
    )

    parser.add_argument(
        "--target-expert-model-parallel-size",
        type=int,
        default=1
    )

    parser.add_argument(
        "--hf-ckpt-path",
        type=str
    )
    parser.add_argument(
        "--convert_checkpoint_from_megatron_to_transformers",
        action="store_true",
        help=(
            "If True, convert a Megatron checkpoint to a Transformers checkpoint. "
            "If False, convert a Transformers checkpoint to a Megatron checkpoint."
        ),
    )

    return parser


def load_megatron_model(args):
    args.tensor_model_parallel_size = args.target_tensor_model_parallel_size

    if args.tensor_model_parallel_size >1:
        args.sequence_parallel = True

    os.makedirs(args.save, exist_ok=True)
    os.system("cp -rf " + args.load + "/config*.json " + args.save)
    os.system("cp -rf " + args.load + "/cpp_kernels.py " + args.save)
    os.system("cp -rf " + args.load + "/generation*.json " + args.save)
    os.system("cp -rf " + args.load + "/modeling*.py " + args.save)
    os.system("cp -rf " + args.load + "/qwen*.py " + args.save)
    os.system("cp -rf " + args.load + "/qwen.tiktoken " + args.save)
    os.system("cp -rf " + args.load + "/tokenization*.py " + args.save)
    os.system("cp -rf " + args.load + "/tokenizer* " + args.save)
    os.system("cp -rf " + args.load + "/configuration_qwen.py " + args.save)


    model = model_provider()


    model_path = args.load
    tracker_filename = get_checkpoint_tracker_filename(model_path)
    iteration, release = read_metadata(tracker_filename)
    head_dim = args.hidden_size // args.num_attention_heads
    group_per_split = args.num_attention_heads // args.tensor_model_parallel_size

    state_dict = {}
    mid_state = defaultdict(list)
    if (
        args.tensor_model_parallel_size == 1
        and args.pipeline_model_parallel_size == 1
    ):
        checkpoint_name = get_checkpoint_name(model_path, iteration, release, None, None, None, None, None)
        state_dict = torch.load(checkpoint_name)['model']

    elif (
        args.tensor_model_parallel_size > 1
        and args.pipeline_model_parallel_size == 1
    ):  
        for tp_rank in range(args.tensor_model_parallel_size):
            checkpoint_name = get_checkpoint_name(model_path, iteration, release, None, tp_rank, None, None, None)
            print(f'load {checkpoint_name}')
            split_state = torch.load(checkpoint_name, map_location="cpu")['model']
            for k, v in split_state.items():
                mid_state[k].append(v)
        for k, v in mid_state.items():
            if not isinstance(v[0], torch.Tensor) or 'norm' in k:
                target_v = v[0]
            elif 'embedding' in k or 'output_layer' in k:
                target_v = torch.cat(v, dim=0)
            elif 'linear_proj' in k or 'linear_fc2' in k:
                target_v = torch.cat(v, dim=1)
            elif 'linear_qkv.weight' in k:
                viewed = [x.view(group_per_split, -1, head_dim, args.hidden_size) for x in v]
                target_v = torch.cat(viewed, dim=0).view(-1, args.hidden_size)
            elif 'linear_qkv.bias' in k:
                viewed = [x.view(group_per_split, -1) for x in v]
                target_v = torch.cat(viewed, dim=0).view(-1)
            elif 'linear_fc1' in k:
                viewed = [x.view(2, -1, args.hidden_size) for x in v]
                target_v = torch.cat(viewed, dim=1).view(-1, args.hidden_size)
            else:
                raise ValueError
            state_dict[k] = target_v
    else:
        raise ValueError('not support yet')

    model.load_state_dict(state_dict)
    return model


def convert_checkpoint_from_megatron_to_transformers(mgmodel, hgmodel, args):

    num_attention_heads = args.num_attention_heads
    hidden_dim = args.hidden_size
    head_dim = hidden_dim // args.num_attention_heads


    with torch.no_grad():
        hgmodel.transformer.wte.weight.copy_(mgmodel.embedding.word_embeddings.weight)
        for mglayer, hglayer in zip(mgmodel.decoder.layers, hgmodel.transformer.h):
            hglayer.ln_1.weight.copy_(mglayer.self_attention.linear_qkv.layer_norm_weight)
            qkv = mglayer.self_attention.linear_qkv.weight
            qkv = megatron_to_transformers_fix_query_key_value_ordering(
                        qkv,
                        3.0,
                        3,
                        num_attention_heads,
                        head_dim,
                    )
            hglayer.attn.c_attn.weight.copy_(qkv)
            qkv_bias = mglayer.self_attention.linear_qkv.bias
            qkv_bias = megatron_to_transformers_fix_query_key_value_ordering(
                        qkv_bias,
                        3.0,
                        3,
                        num_attention_heads,
                        head_dim,
                    )
            hglayer.attn.c_attn.bias.copy_(qkv_bias)
            hglayer.attn.c_proj.weight.copy_(mglayer.self_attention.linear_proj.weight)
            fc1_weight = mglayer.mlp.linear_fc1.weight
            w2_weight, w1_weight = torch.split(fc1_weight ,split_size_or_sections=args.ffn_hidden_size)
            hglayer.mlp.w2.weight.copy_(w2_weight)
            hglayer.mlp.w1.weight.copy_(w1_weight)
            hglayer.mlp.c_proj.weight.copy_(mglayer.mlp.linear_fc2.weight)
            hglayer.ln_2.weight.copy_(mglayer.mlp.linear_fc1.layer_norm_weight)
        hgmodel.transformer.ln_f.weight.copy_(mgmodel.decoder.final_layernorm.weight)
        hgmodel.lm_head.weight.copy_(mgmodel.output_layer.weight)
def megatron_to_transformers_fix_query_key_value_ordering(
        param, checkpoint_version, num_splits, num_heads, hidden_size
):
    """
    Permutes layout of param tensor to [num_splits * num_heads * hidden_size, :] for compatibility with later versions
    of NVIDIA Megatron-LM. The inverse operation is performed inside Megatron-LM to read checkpoints:
    https://github.com/NVIDIA/Megatron-LM/blob/v2.4/megatron/checkpointing.py#L209 If param is the weight tensor of the
    self-attention block, the returned tensor will have to be transposed one more time to be read by HuggingFace GPT2.
    This function is taken from `convert_megatron_gpt2_checkpoint.py`
    Args:
        param (torch.Tensor): the tensor to permute
        checkpoint_version (int): the version of the checkpoint.
        num_splits (int): the number of projections, usually 3 for (Query, Key, Value)
        num_heads (int): the number of attention heads
        hidden_size (int): the hidden size per head
    """

    input_shape = param.size()
    if checkpoint_version == 1.0:
        # version 1.0 stores [num_heads * hidden_size * num_splits, :]
        saved_shape = (num_heads, hidden_size, num_splits) + input_shape[1:]
        param = param.view(*saved_shape)
        param = param.transpose(0, 2)
        param = param.transpose(1, 2).contiguous()
    elif checkpoint_version >= 2.0:
        # other versions store [num_heads * num_splits * hidden_size, :]
        saved_shape = (num_heads, num_splits, hidden_size) + input_shape[1:]
        param = param.view(*saved_shape)
        param = param.transpose(0, 1).contiguous()
    param = param.view(*input_shape)
    return param

def transformers_to_megatron_fix_query_key_value_ordering(
    param, checkpoint_version, num_splits, num_heads, hidden_size
):
    """
    Permutes layout of param tensor to the one compatible with respective NVIDIA Megatron-LM chekpoint versions. Input
    is [num_splits * num_heads * hidden_size, :] and output is [num_heads * hidden_size * num_splits, :] for version
    1.0 and [num_heads * num_splits * hidden_size, :] for version 2.0 and later. If param is the weight tensor of the
    self-attention block, the param needs to be already transposed before calling this function.
    Args:
        param (torch.Tensor): the tensor to permute
        checkpoint_version (int): the version of the checkpoint.
        num_splits (int): the number of projections, usually 3 for (Query, Key, Value)
        num_heads (int): the number of attention heads
        hidden_size (int): the hidden size per head
    """

    # Input is [num_splits * num_heads * hidden_size, :]
    input_shape = param.size()
    if checkpoint_version == 1.0:
        # version 1.0 stores [num_heads * hidden_size * num_splits, :]
        current_shape = (num_splits, num_heads, hidden_size) + input_shape[1:]
        param = param.view(*current_shape)
        param = param.transpose(0, 2)
        param = param.transpose(1, 2).contiguous()
    elif checkpoint_version >= 2.0:
        # other versions store [num_heads * num_splits * hidden_size, :]
        current_shape = (num_splits, num_heads, hidden_size) + input_shape[1:]
        param = param.view(*current_shape)
        param = param.transpose(0, 1).contiguous()
    param = param.view(*input_shape)
    return param

def convert_checkpoint_from_transformers_to_megatron(hgmodel, mgmodel, args):
    num_attention_heads = args.num_attention_heads
    hidden_dim = args.hidden_size
    head_dim = hidden_dim // args.num_attention_heads
    num_experts = args.num_experts
    with torch.no_grad():
        mgmodel.embedding.word_embeddings.weight.copy_(hgmodel.transformer.wte.weight)
        for mglayer, hglayer in zip(mgmodel.decoder.layers, hgmodel.transformer.h):
            mglayer.self_attention.linear_qkv.layer_norm_weight.copy_(hglayer.ln_1.weight)
            qkv = hglayer.attn.c_attn.weight
            
            qkv = transformers_to_megatron_fix_query_key_value_ordering(
                        qkv,
                        3.0,
                        3,
                        num_attention_heads,
                        head_dim,
                    )
            mglayer.self_attention.linear_qkv.weight.copy_(qkv)
            qkv_bias = hglayer.attn.c_attn.bias
            qkv_bias = transformers_to_megatron_fix_query_key_value_ordering(
                        qkv_bias,
                        3.0,
                        3,
                        num_attention_heads,
                        head_dim,
                    )
            mglayer.self_attention.linear_qkv.bias.copy_(qkv_bias)
            mglayer.self_attention.linear_proj.weight.copy_(hglayer.attn.c_proj.weight)
            
            fc1_weight = torch.cat([hglayer.mlp.w2.weight, hglayer.mlp.w1.weight])
            mglayer.mlp.linear_fc1.weight.copy_(fc1_weight)
            mglayer.mlp.linear_fc2.weight.copy_(hglayer.mlp.c_proj.weight)
            mglayer.mlp.linear_fc1.layer_norm_weight.copy_(hglayer.ln_2.weight)

        mgmodel.decoder.final_layernorm.weight.copy_(hgmodel.transformer.ln_f.weight)
        mgmodel.output_layer.weight.copy_(hgmodel.lm_head.weight)


def save_state_dict(args, model, checkpoint_name):
    state_dict = {}
    state_dict['args'] = args
    state_dict['checkpoint_version'] = 3.0
    state_dict['iteration'] = 0    
    state_dict['model'] = model
    os.makedirs(os.path.dirname(checkpoint_name), exist_ok=True)
    print(f'save model part {checkpoint_name}')
    torch.save(state_dict, checkpoint_name)



def save_mgmodel(mgmodel, args):
    args.tensor_model_parallel_size = args.target_tensor_model_parallel_size

    os.makedirs(args.save, exist_ok=True)
    os.system("cp -rf " + args.load + "/config*.json " + args.save)
    os.system("cp -rf " + args.load + "/cpp_kernels.py " + args.save)
    os.system("cp -rf " + args.load + "/generation*.json " + args.save)
    os.system("cp -rf " + args.load + "/modeling*.py " + args.save)
    os.system("cp -rf " + args.load + "/qwen*.py " + args.save)
    os.system("cp -rf " + args.load + "/qwen.tiktoken " + args.save)
    os.system("cp -rf " + args.load + "/tokenization*.py " + args.save)
    os.system("cp -rf " + args.load + "/tokenizer* " + args.save)
    os.system("cp -rf " + args.load + "/configuration_qwen.py " + args.save)

    tracker_filepath = os.path.join(args.save, 'latest_checkpointed_iteration.txt')
    with open(tracker_filepath, "w") as f:
        f.write("release")

    head_dim = args.hidden_size // args.num_attention_heads
    group_per_split = args.num_attention_heads // args.tensor_model_parallel_size
    full_model = mgmodel.state_dict_for_save_checkpoint()
    # print(full_model.keys())
    # for k in list(full_model.keys()):
    #     if full_model[k] is None or "_extra_state" in k:
    #         full_model.pop(k)

    if (
        args.tensor_model_parallel_size == 1
        and args.pipeline_model_parallel_size == 1
    ):
        checkpoint_name = get_checkpoint_name(args.save, 0, True)
        save_state_dict(args, full_model, checkpoint_name)
    elif (
        args.tensor_model_parallel_size > 1
        and args.pipeline_model_parallel_size == 1
    ):
        for tp_rank in range(args.tensor_model_parallel_size):
            model_split = {}
            checkpoint_name = get_checkpoint_name(args.save, 0, True, None, tp_rank)
            print(f'tensor_parallel, save model to {checkpoint_name}')
            for k, v in full_model.items():
                if not isinstance(v, torch.Tensor):
                    target_v = v
                elif 'linear_qkv.weight' in k and 'norm' not in k:
                    viewed = v.view(args.num_attention_heads, -1, head_dim, args.hidden_size)
                    viewed = viewed[group_per_split*tp_rank : group_per_split*(tp_rank + 1)]
                    target_v = viewed.view(-1, args.hidden_size)
                elif 'linear_qkv.bias' in k and 'norm' not in k:
                    viewed = v.view(args.num_attention_heads, -1, head_dim)
                    viewed = viewed[group_per_split * tp_rank: group_per_split * (tp_rank + 1)]
                    target_v = viewed.view(-1)
                elif 'linear_proj' in k or 'linear_fc2' in k:
                    seg = v.shape[1] // args.tensor_model_parallel_size
                    target_v = v[:, seg*tp_rank : seg*(tp_rank + 1)]
                elif 'embedding' in k or 'output_layer' in k:
                    seg = v.shape[0] // args.tensor_model_parallel_size
                    target_v = v[seg*tp_rank : seg*(tp_rank + 1)]
                elif 'linear_fc1' in k and 'norm' not in k:
                    viewed = v.view(-1, args.ffn_hidden_size, args.hidden_size)
                    seg = args.ffn_hidden_size // args.tensor_model_parallel_size
                    target_v = viewed[:, seg*tp_rank: seg*(tp_rank+1), :].reshape(-1, args.hidden_size)
                else:
                    target_v = v
                model_split[k] = target_v
            save_state_dict(args, model_split, checkpoint_name)
    else:
        raise ValueError('not support pp convert')
    print(f'megatron model is save to {args.save}')


def save_hgmodel(args, model):
    output_state_dict = model.state_dict()
    max_shard_size = "10GB"
    shards, index = shard_checkpoint(output_state_dict, max_shard_size=max_shard_size)
    os.makedirs(args.save, exist_ok=True)
    for shard_file, shard in shards.items():
        target_file = os.path.join(args.save, shard_file)
        print(f'huggingface model is save to {target_file}')
        torch.save(shard, target_file)

    if index is None:
        print(f"Model weights saved in {os.path.join(args.save, WEIGHTS_NAME)}")
    else:
        save_index_file = os.path.join(args.save, WEIGHTS_INDEX_NAME)
        # Save the index as well
        with open(save_index_file, "w", encoding="utf-8") as f:
            content = json.dumps(index, indent=2, sort_keys=True) + "\n"
            f.write(content)
        print(
            f"The model is bigger than the maximum size per checkpoint ({max_shard_size}) and is going to be "
            f"split in {len(shards)} checkpoint shards. You can find where each parameters has been saved in the "
            f"index located at {save_index_file}."
        )


def add_extra_args(parser):
    parser = get_patch_args(parser)
    parser = add_model_args(parser)
    return parser

#     return config, model.eval()
def main():
    initialize_megatron(extra_args_provider=add_extra_args)
    args = get_args()

    if args.convert_checkpoint_from_megatron_to_transformers:
        mg_model = load_megatron_model(args)
        print("mg_model load success")
        print("args.hf_ckpt_path",args.hf_ckpt_path)
        hf_model = AutoModelForCausalLM.from_config(config=AutoConfig.from_pretrained(args.load, trust_remote_code=True),trust_remote_code=True)
        convert_checkpoint_from_megatron_to_transformers(mg_model, hf_model, args)
        save_hgmodel(args, hf_model)
    else:
        hf_model = AutoModelForCausalLM.from_pretrained(args.load, trust_remote_code=True)  
        print(hf_model)
        mg_model = model_provider()
        print(mg_model.vocab_size)
        convert_checkpoint_from_transformers_to_megatron(hf_model, mg_model, args)
        save_mgmodel(mg_model, args)

if __name__ == "__main__":
    main()
