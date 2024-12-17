#!/bin/bash

# help information
print_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -w,  --world_size_1             Set the world size for distributed training (1, 2, 4 or 8)"
    echo "  -sc,  --src_ckpt_path_1         Source ckpt path"
    echo "  -dc,  --dst_ckpt_path_1         Destination ckpt path"
    echo "  -h,  --help                     Print this help message"
}

# parser args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -w|--world_size_1) world_size_1="$2"; shift ;;
        -sc|--src_ckpt_path_1) src_ckpt_path_1="$2"; shift ;;
        -dc|--dst_ckpt_path_1) dst_ckpt_path_1="$2"; shift ;;
        -h|--help) print_usage; exit 0 ;;
        *) echo "Unknown option: $1"; print_usage; exit 1 ;;
    esac
    shift
done

yaml_path_1=$CONVERT_PATH/model/llama2_7b/noqkv/llama2_7b_${world_size_1}p.yaml
echo "yaml 文件路径为：$yaml_path_1"

infer_strategy_file_1=$dst_ckpt_path_1/strategy/llama2_7b/noqkv/${world_size_1}_llama-2-7b
mkdir -p $infer_strategy_file_1
echo "strategy 路径保存在： $infer_strategy_file_1 "

if [ ! -e $dst_ckpt_path_1 ]; then
    mkdir -p $dst_ckpt_path_1
    echo "已创建目标路径：$dst_ckpt_path_1"
fi

bash $CONVERT_PATH/convert_ckpt_noqkv/ckpt_convert.sh \
    --function distributed_weight_transfer \
    --precision  fp16 \
    --world_size  $world_size_1 \
    --yaml_path  $yaml_path_1 \
    --src_ckpt_path $src_ckpt_path_1 \
    --dst_ckpt_path $dst_ckpt_path_1 \
    --infer_strategy_file $infer_strategy_file_1

if [ "$word_size_1" == "16" ]; then
    # 如果 word_size 等于 16，执行特定的脚本
    source $CONVERT_PATH/env/set_2n_env.sh
    bash ckpt_convert_for_16p.sh \
    -f distributed_weight_transfer \
    -p fp16 \
    -w $world_size_1 \
    -is $infer_strategy_file_1 \
    -sc $src_ckpt_path_1 \
    -dc $dst_ckpt_path_1 \
    -y $yaml_path_1
fi