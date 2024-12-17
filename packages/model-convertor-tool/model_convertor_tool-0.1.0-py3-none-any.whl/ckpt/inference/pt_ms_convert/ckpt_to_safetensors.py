""" adjust qkv layout for quant transform different card numbers """

import argparse
from datetime import datetime
import mindspore as ms


def main(args):
    """transform ckpt to safetensors"""
    start_time = datetime.now().strftime("%H:%M:%S")
    ms.ckpt_to_safetensors(file_path=args.src_ckpt_path, save_path=args.dst_safetensors_path)
    end_time = datetime.now().strftime("%H:%M:%S")
    # 打印开始和结束时间
    print(f"convert finished, start time: {start_time}, End time: {end_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_ckpt_path', default='', type=str,
                        help='ckpt path.')
    parser.add_argument('--dst_safetensors_path', default='', type=str,
                        help='safetensors path.')
    uargs = parser.parse_args()

    main(uargs)
