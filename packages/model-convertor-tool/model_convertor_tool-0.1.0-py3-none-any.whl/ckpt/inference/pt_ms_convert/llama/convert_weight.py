# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
Convert llama weight.
Support huggingface format and Meta format.
"""

import os
import json
import argparse
from pathlib import Path

import numpy as np
import mindspore as ms
from mindspore import ops

from mindformers.tools.utils import str2bool
from mindformers.utils.convert_utils import pt2ms


def convert_meta_torch_ckpt(ckpt_dir, output_name, dtype=ms.float16):
    """Support convert meta weight splited."""
    print(f"Trying to convert pytorch checkpoint in '{ckpt_dir}'.", flush=True)
    try:
        from torch import load
    except:
        raise ImportError(f"Failed to load pytorch checkpoint. Please make sure pytorch is available.")
    dic = {
        'tok_embeddings.weight': 1,
        'norm.weight': None,
        'output.weight': 0,
        'attention.wq.weight': 0,
        'attention.wk.weight': 0,
        'attention.wv.weight': 0,
        'attention.wo.weight': 1,
        'feed_forward.w1.weight': 0,
        'feed_forward.w2.weight': 1,
        'feed_forward.w3.weight': 0,
        'attention_norm.weight': None,
        'ffn_norm.weight': None,
        'rope.freqs': None,
    }
    ckpt_paths = sorted(Path(ckpt_dir).glob("*.pth"))
    if not ckpt_paths:
        print(f"Do not find pytorch checkpoint in '{ckpt_dir}'.", flush=True)
        return False
    with open(Path(ckpt_dir) / "params.json", "r") as f:
        model_args = json.loads(f.read())
    n_heads = model_args["n_heads"]
    dim = model_args["dim"]

    def permute(w):
        return w.view(n_heads, dim // n_heads // 2, 2, dim).transpose(1, 2).reshape(dim, dim)

    checkpoints = []
    for i in range(len(ckpt_paths)):
        checkpoints.append(load(ckpt_paths[i], map_location="cpu"))
    ckpt_list = []
    for name in checkpoints[0].keys():
        for k, v in dic.items():
            if k in name:
                if v is not None:
                    value = np.concatenate(
                        [checkpoints[i][name].numpy() for i in range(len(checkpoints))], v)
                else:
                    value = checkpoints[0][name].numpy()
        if name == 'norm.weight':
            name = 'norm_out.weight'
        if name == 'output.weight':
            name = 'lm_head.weight'
        else:
            name = 'model.' + name
        if 'rope.freqs' in name:
            continue

        if 'wq' in name or 'wk' in name:
            value = permute(value)
        print(f'\rprocessing parameter: {name} {value.shape}     ', end='', flush=True)
        ckpt_list.append({'name': name, 'data': ms.Tensor(value, dtype=dtype)})

    ckpt_file = os.path.join(ckpt_dir, output_name)
    ms.save_checkpoint(ckpt_list, ckpt_file)
    print(f"\rConvert pytorch checkpoint finished, the mindspore checkpoint is saved in '{ckpt_file}'.", flush=True)
    return True


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def name_replace(name: str):
    """replace hf param name to ms."""
    name = name.replace('embed_tokens.weight', 'tok_embeddings.embedding_weight')
    name = name.replace('.self_attn.q_proj.', '.attention.wq.')
    name = name.replace('.self_attn.k_proj.', '.attention.wk.')
    name = name.replace('.self_attn.v_proj.', '.attention.wv.')
    name = name.replace('.self_attn.o_proj.', '.attention.wo.')
    name = name.replace('.mlp.gate_proj.', '.feed_forward.w1.')
    name = name.replace('.mlp.down_proj.', '.feed_forward.w2.')
    name = name.replace('.mlp.up_proj.', '.feed_forward.w3.')
    name = name.replace('.input_layernorm.', '.attention_norm.')
    name = name.replace('.post_attention_layernorm.', '.ffn_norm.')
    name = name.replace('.norm.', '.norm_out.')
    return name

# pylint: disable=W0613
def convert_pt_to_ms(input_path, output_path, dtype=None, **kwargs):
    """convert hf weight to ms."""
    print(f"Trying to convert huggingface checkpoint in '{input_path}'.", flush=True)
    try:
        from transformers import LlamaForCausalLM
    except:
        raise ImportError(f"Failed to load huggingface checkpoint. Please make sure transformers is available.")

    try:
        model_hf = LlamaForCausalLM.from_pretrained(os.path.dirname(input_path))
    # pylint: disable=W0703
    except Exception as e:
        print(f"Do not find huggingface checkpoint in '{os.path.dirname(input_path)}', Error {e.message}.", flush=True)
        return False
    ckpt_list = []
    for name, value in model_hf.state_dict().items():
        name = name_replace(name)
        if name == 'norm.weight':
            name = 'norm_out.weight'
        if name[:7] == 'layers.':
            name = name[7:]

        print(f'\rprocessing parameter: {name} {value.shape}     ', end='', flush=True)
        ckpt_list.append({'name': name, 'data': pt2ms(value, dtype)})

    ms.save_checkpoint(ckpt_list, output_path)
    print(f"\rConvert huggingface checkpoint finished, the mindspore checkpoint is saved in '{output_path}'.",
          flush=True)
    return True


def convert_to_new_ckpt(ckpt_path, config_path):
    """convert previous ckpt to new ckpt"""
    load_path = ckpt_path.split('.ckpt')[0]
    save_path = load_path + "_hf"
    params = ms.load_checkpoint(load_path.split('.ckpt')[0] + '.ckpt')
    with open(config_path, "r") as f:
        model_args = json.loads(f.read())
    n_heads = model_args["n_heads"]
    dim = model_args["dim"]

    def permute(w):
        return ops.transpose(w.reshape(n_heads, dim // n_heads // 2, 2, dim), (0, 2, 1, 3)).reshape(dim, dim)

    ckpt_list = []
    for name in params.keys():
        value = params[name].value()
        if '.wq' in name or '.wk' in name:
            value = permute(value)
        ckpt_list.append({'name': name, 'data': value})
        print("\r", name, value.shape, end="               ")

    ms.save_checkpoint(ckpt_list, save_path)


def convert_qkv_concat_weight(param_dict):
    """convert qkv concat weight"""
    assume_num_layers = 500
    for i in range(assume_num_layers):
        # qkv weight concat
        wq_weight_name = f"model.layers.{i}.attention.wq.weight"
        wk_weight_name = f"model.layers.{i}.attention.wk.weight"
        wv_weight_name = f"model.layers.{i}.attention.wv.weight"
        qkv_concat_weight_name = f"model.layers.{i}.attention.w_qkv.weight"
        if wq_weight_name not in param_dict:
            break
        wq_weight = param_dict[wq_weight_name].asnumpy()
        wk_weight = param_dict[wk_weight_name].asnumpy()
        wv_weight = param_dict[wv_weight_name].asnumpy()
        qkv_weight = np.concatenate((wq_weight, wk_weight, wv_weight), 0)
        param_dict[qkv_concat_weight_name] = ms.Parameter(qkv_weight, name=qkv_concat_weight_name)

        # gate hidden weight concat
        ffn_gate_weight_name = f"model.layers.{i}.feed_forward.w1.weight"
        ffn_hidden_weight_name = f"model.layers.{i}.feed_forward.w3.weight"
        gate_hidden_concat_weight_name = f"model.layers.{i}.feed_forward.w_gate_hidden.weight"

        ffn_gate_weight = param_dict[ffn_gate_weight_name].asnumpy()
        ffn_hidden_weight = param_dict[ffn_hidden_weight_name].asnumpy()
        gate_hidden_weight = np.concatenate((ffn_gate_weight, ffn_hidden_weight), 0)
        param_dict[gate_hidden_concat_weight_name] = ms.Parameter(gate_hidden_weight,
                                                                  name=gate_hidden_concat_weight_name)

        param_dict.pop(wq_weight_name)
        param_dict.pop(wk_weight_name)
        param_dict.pop(wv_weight_name)
        param_dict.pop(ffn_gate_weight_name)
        param_dict.pop(ffn_hidden_weight_name)
        print("transform: {}".format(qkv_concat_weight_name))
        print("transform: {}".format(gate_hidden_concat_weight_name))

    for i in range(assume_num_layers):
        # qkv bias concat
        wq_bias_name = f"model.layers.{i}.attention.wq.bias"
        wk_bias_name = f"model.layers.{i}.attention.wk.bias"
        wv_bias_name = f"model.layers.{i}.attention.wv.bias"
        qkv_concat_bias_name = f"model.layers.{i}.attention.w_qkv.bias"
        if wq_bias_name not in param_dict:
            break

        wq_bias_weight = param_dict[wq_bias_name].asnumpy()
        wk_bias_weight = param_dict[wk_bias_name].asnumpy()
        wv_bias_weight = param_dict[wv_bias_name].asnumpy()
        qkv_bias_weight = np.concatenate((wq_bias_weight, wk_bias_weight, wv_bias_weight), 0)
        param_dict[qkv_concat_bias_name] = ms.Parameter(qkv_bias_weight, name=qkv_concat_bias_name)

        param_dict.pop(wq_bias_name)
        param_dict.pop(wk_bias_name)
        param_dict.pop(wv_bias_name)
        print("transform: {}".format(qkv_concat_bias_name))
    return param_dict


def convert_to_qkv_concat(pre_ckpt_path, mindspore_ckpt_path):
    """convert previous ckpt to qkv concat ckpt"""
    if os.path.isdir(pre_ckpt_path):
        rank_dir_list = os.listdir(pre_ckpt_path)
        for rank_dir in rank_dir_list:
            rank_dir_name = str(rank_dir)
            rank_id = rank_dir_name.split("_")[1]
            checkpoint_path = os.path.join(pre_ckpt_path, rank_dir_name, "checkpoint_{}.ckpt".format(rank_id))
            print("checkpoint_path: {}".format(checkpoint_path))
            params = ms.load_checkpoint(checkpoint_path)
            params = convert_qkv_concat_weight(params)

            save_dir = os.path.join(mindspore_ckpt_path, rank_dir_name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = os.path.join(mindspore_ckpt_path, rank_dir_name, "checkpoint_{}.ckpt".format(rank_id))
            ms.save_checkpoint(params, save_path)
    else:
        params = ms.load_checkpoint(pre_ckpt_path)
        params = convert_qkv_concat_weight(params)
        ms.save_checkpoint(params, mindspore_ckpt_path)


def adjust_quant_qkv_concat(src_dir, dst_dir, src_tp=4, dst_tp=2):
    def find_ckpts(base_path):
        index = 0
        ckpts = []
        while True:
            cur_dir = os.path.join(base_path, f"rank_{index}")
            index += 1
            if not os.path.isdir(cur_dir):
                break
            all_file = os.listdir(cur_dir)
            ckpt_files = [file for file in all_file if file.endswith(".ckpt")]
            if len(ckpt_files) != 1:
                raise RuntimeError(f"Only one ckpt file should be exist under each rank_i dir, but got {len(ckpt_files)} ckpt files under {cur_dir}.")
            ckpts.append(os.path.join(cur_dir, ckpt_files[0]))
        return ckpts

    def adjust_single_param(params_dict, param_name, group, is_qkv):
        if param_name not in params_dict:
            return False
        print(f"Processing {param_name}...", flush=True)
        param = params_dict[param_name].asnumpy()
        total = param.shape[0]
        group_members = 3 if is_qkv else 2
        segment = total // group // group_members
        member0 = []
        member1 = []
        member2 = []
        for j in range(group):
            p0 = (j * group_members + 0) * segment
            p1 = (j * group_members + 1) * segment
            p2 = (j * group_members + 2) * segment
            member0.append(param[p0 : p1,])
            member1.append(param[p1 : p2,])
            if is_qkv:
                p3 = (j * group_members + 3) * segment
                member2.append(param[p2 : p3,])
        if is_qkv:
            orderd_list = member0 + member1 + member2
        else: # ffn
            orderd_list = member0 + member1
        params_dict[param_name] = ms.Parameter(np.concatenate(orderd_list, 0), name=param_name)
        return True

    def adjust_single_ckpt(src_ckpt_file, dst_ckpt_file, src_tp=4, dst_tp=2):
        group = src_tp // dst_tp
        if group == 0:
            raise ValueError(f"Invalid src_tp({src_tp}) and dst_tp({dst_tp}).")
        print(f"Loading {src_ckpt_file}...", flush=True)
        params_dict = ms.load_checkpoint(src_ckpt_file)
        changed = False
        i = 0
        while True:
            changed = False
            # qkv weight adjust
            qkv_weight_name = f"model.layers.{i}.attention.w_qkv._handler.weight"
            changed |= adjust_single_param(params_dict, qkv_weight_name, group, True)
            # qkv bias adjust
            qkv_bias_name = f"model.layers.{i}.attention.w_qkv._handler.bias"
            changed |= adjust_single_param(params_dict, qkv_bias_name, group, True)
            # qkv output quantizer scale adjust
            qkv_oqscale_name = f"model.layers.{i}.attention.w_qkv._output_quantizer.scale"
            changed |= adjust_single_param(params_dict, qkv_oqscale_name, group, True)
            # qkv weight quantizer scale adjust
            qkv_wscale_name = f"model.layers.{i}.attention.w_qkv._weight_quantizer.scale"
            changed |= adjust_single_param(params_dict, qkv_wscale_name, group, True)
            # qkv weight quantizer zp adjust
            qkv_wzp_name = f"model.layers.{i}.attention.w_qkv._weight_quantizer.zp_neg"
            changed |= adjust_single_param(params_dict, qkv_wzp_name, group, True)
            # ffn weight adjust
            ffn_weight_name = f"model.layers.{i}.feed_forward.w_gate_hidden._handler.weight"
            changed |= adjust_single_param(params_dict, ffn_weight_name, group, False)
            # ffn bias adjust
            ffn_bias_name = f"model.layers.{i}.feed_forward.w_gate_hidden._handler.bias"
            changed |= adjust_single_param(params_dict, ffn_bias_name, group, False)
            # ffn output quantizer scale adjust
            ffn_oqscale_name = f"model.layers.{i}.feed_forward.w_gate_hidden._output_quantizer.scale"
            changed |= adjust_single_param(params_dict, ffn_oqscale_name, group, False)
            # ffn weight quantizer scale adjust
            ffn_wscale_name = f"model.layers.{i}.feed_forward.w_gate_hidden._weight_quantizer.scale"
            changed |= adjust_single_param(params_dict, ffn_wscale_name, group, False)
            # ffn weight quantizer zp adjust
            ffn_wzp_name = f"model.layers.{i}.feed_forward.w_gate_hidden._weight_quantizer.zp_neg"
            changed |= adjust_single_param(params_dict, ffn_wzp_name, group, False)
            if changed:
                i += 1
            else:
                break
        ms.save_checkpoint(params_dict, dst_ckpt_file)
        print(f"Saved ckpt file: {dst_ckpt_file}.", flush=True)

    ckpt_files = find_ckpts(src_dir)
    if not ckpt_files:
        print(f"Can not find and ckpt files under {src_dir}.", flush=True)
    os.makedirs(dst_dir, exist_ok=True)
    for i in range(len(ckpt_files)):
        src_ckpt_file = ckpt_files[i]
        dst_ckpt_file = os.path.join(dst_dir, f"rank_{i}")
        os.makedirs(dst_ckpt_file, exist_ok=True)
        dst_ckpt_file = os.path.join(dst_ckpt_file, f"checkpoint_{i}.ckpt")
        adjust_single_ckpt(src_ckpt_file, dst_ckpt_file, src_tp, dst_tp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--torch_ckpt_path', default='./llama_model/llama-13b-hf/hf.bin')
    parser.add_argument('--mindspore_ckpt_path', default='transform.ckpt')
    parser.add_argument('--pre_ckpt_path', default=None)
    parser.add_argument('--config_path', default=None)
    parser.add_argument('--qkv_concat', default=False, type=str2bool)
    parser.add_argument('--quant_qkv_concat_adjust', type=str, help="Adjust ckpt after qkv-concat ckpt being quantizerd. Avaliable: 4t2, 8t4.")
    args = parser.parse_args()

    if args.quant_qkv_concat_adjust:
        if args.quant_qkv_concat_adjust == "4t2":
            adjust_quant_qkv_concat(args.pre_ckpt_path, args.mindspore_ckpt_path, 4, 2)
        elif args.quant_qkv_concat_adjust == "8t4":
            adjust_quant_qkv_concat(args.pre_ckpt_path, args.mindspore_ckpt_path, 8, 4)
        else:
            raise ValueError(f"Invalid quant_qkv_concat_adjust: {args.quant_qkv_concat_adjust}. Avaliable: 4t2, 8t4.")
    elif args.qkv_concat:
        convert_to_qkv_concat(args.pre_ckpt_path, args.mindspore_ckpt_path)
    elif args.pre_ckpt_path is not None and args.config_path is not None:
        convert_to_new_ckpt(args.pre_ckpt_path, args.config_path)
    else:
        convert_pt_to_ms(input_path=args.torch_ckpt_path, output_path=args.mindspore_ckpt_path)
