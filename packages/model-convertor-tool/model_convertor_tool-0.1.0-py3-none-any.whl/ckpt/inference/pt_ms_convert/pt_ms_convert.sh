#!/bin/bash

# help information
print_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -f,  --function               Set bin2ckpt or ckpt2sft or ckpt2pth"
    echo "  -sc,  --src_ckpt_path         Source ckpt path"
    echo "  -dc,  --dst_ckpt_path         Destination ckpt path"
    echo "  -h,  --help                   Print this help message"
}

# parser args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--function) function="$2"; shift ;;
        -sc|--src_ckpt_path) src_ckpt_path="$2"; shift ;;
        -dc|--dst_ckpt_path) dst_ckpt_path="$2"; shift ;;
        -h|--help) print_usage; exit 0 ;;
        *) echo "Unknown option: $1"; print_usage; exit 1 ;;
    esac
    shift
done

# 传参校验
if [ -z "$function" ] || [ -z "$src_ckpt_path" ] ||  [ -z "$dst_ckpt_path" ]; then
    echo "Error: Missing function src_ckpt_path and dst_ckpt_path"
    exit 1
fi

# 输出路径处理
if [[ $dst_ckpt_path == */ ]]; then
  dst_ckpt_path=${dst_ckpt_path%*/}
fi

if [ ! -e $dst_ckpt_path ]; then
    mkdir -p $dst_ckpt_path
    echo "已创建目标路径：$dst_ckpt_path"
fi

if [ "$function" == "bin2ckpt" ]; then
    # 在src路径末尾添加“/”
    if [[ $src_ckpt_path != */ ]]; then
      src_ckpt_path=${src_ckpt_path}/
    fi
    mkdir -p $dst_ckpt_path/rank_0

#    python convert_weight.py \
#    --model llama \
#    --input_path $src_ckpt_path \
#    --output_path $dst_ckpt_path/rank_0/llama2_7b \
#    --dtype fp16

    python $CONVERT_PATH/pt_ms_convert/convert_pt2ms.py \
    --torch_ckpt_dir $src_ckpt_path \
    --mindspore_ckpt_file $dst_ckpt_path/rank_0/llama2_7b.ckpt


elif [ "$function" == "ckpt2pth" ]; then
  if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
  echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
  exit 1
  fi

  python $CONVERT_PATH/pt_ms_convert/convert_weight.py \
  --model llama \
  --reversed \
  --input_path $src_ckpt_path \
  --output_path $dst_ckpt_path/llama2.pth

elif [ "$function" == "ckpt2sft" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi

    python $CONVERT_PATH/pt_ms_convert/trans_layers_name.py \
    --mindspore_ckpt_path $src_ckpt_path \
    --torch_ckpt_path $dst_ckpt_path/trans_llama2_7b.ckpt
    echo "修改ckpt模型名称成功"

    python $CONVERT_PATH/pt_ms_convert/ckpt_to_safetensors.py \
    --src_ckpt_path $dst_ckpt_path/trans_llama2_7b.ckpt  \
    --dst_safetensors_path $dst_ckpt_path

    rm -rf $dst_ckpt_path/trans_llama2_7b.ckpt
fi

echo "checkpoint convert fnished."
