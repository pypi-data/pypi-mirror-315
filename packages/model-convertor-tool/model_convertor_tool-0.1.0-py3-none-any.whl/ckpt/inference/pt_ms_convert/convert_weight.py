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
"""convert weight."""
import argparse
import copy
import importlib

import torch
import mindspore as ms

dtype_map = {
    'fp32': ms.float32,
    'bf16': ms.bfloat16,
    'fp16': ms.float16
}
reversed_dtype_map = {
    'fp32': torch.float32,
    'bf16': torch.bfloat16,
    'fp16': torch.float16
}

convert_map = {
    'llama': 'llama.convert_weight.convert_pt_to_ms',
}
reversed_convert_map = {
    'llama': 'llama.convert_reversed.convert_ms_to_pt',
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default=None, required=True, help='model name')
    parser.add_argument('--reversed', action='store_true', help="convert ms to hf")
    parser.add_argument('--input_path', default=None, type=str, required=True)
    parser.add_argument('--output_path', default=None, type=str, required=True)
    parser.add_argument('--dtype', default=None, type=str, required=False)

    parser.add_argument('--n_head', default=32, type=int, required=False,
                        help="Only for bloom, 16 for bloom_560m or 32 for bloom_7.1b")
    parser.add_argument('--hidden_size', default=4096, type=int, required=False,
                        help="Only for bloom, 1024 for bloom_560m or 4096 for bloom_7.1b")
    parser.add_argument('--layers', default=12, type=int, required=False,
                        help="Only for gpt2 and wizardcoder. "
                             "The number of layers of the model to be converted from hf to ms")
    parser.add_argument('--is_pretrain', default=False, type=bool, required=False,
                        help="Only for swin. Convert pretrain model weight.")
    parser.add_argument('--telechat_type', default="telechat_12b", type=str, required=False,
                        help="Only for telechat. Telechat version.")
    args, extra_args = parser.parse_known_args()
    extra_args = [i for item in extra_args for i in item.split("=")]

    extra_kwargs = copy.copy(vars(args))
    extra_kwargs.pop('model')
    extra_kwargs.pop('reversed')
    extra_kwargs.pop('input_path')
    extra_kwargs.pop('output_path')
    extra_kwargs.pop('dtype')
    while extra_args:
        key = extra_args.pop(0)
        value = extra_args.pop(0)
        if not key.startswith("--"):
            raise ValueError("Custom config key need to start with --.")
        extra_kwargs[key[2:]] = value

    if args.reversed:
        module_func = reversed_convert_map.get(args.model)
        dtype = reversed_dtype_map.get(args.dtype)
    else:
        module_func = convert_map.get(args.model)
        dtype = dtype_map.get(args.dtype)

    if not module_func:
        raise ValueError(f"Model:{args.model} is not supported!\nSupported Models:{','.join(convert_map.keys())}.")
    if args.dtype and not dtype:
        raise ValueError(f"Dtype:{args.dtype} is not supported!\nSupported Models:{','.join(dtype_map.keys())}.\n")

    model_name, func_name = module_func.rsplit('.', 1)
    convert_func = getattr(importlib.import_module(model_name), func_name)
    convert_func(input_path=args.input_path, output_path=args.output_path, dtype=dtype, **extra_kwargs)
