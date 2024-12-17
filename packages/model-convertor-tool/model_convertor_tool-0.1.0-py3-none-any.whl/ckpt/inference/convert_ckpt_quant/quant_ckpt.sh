#!/bin/bash


# parser args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--precision) precision="$2"; shift ;;
        -y|--yaml_path) yaml_path="$2"; shift ;;
        -d|--dataset_name) dataset_name="$2"; shift ;;
        -dp|--dataset_path) dataset_path="$2"; shift ;;
        -is|--infer_strategy_file) infer_strategy_file="$2"; shift ;;
        -sc|--src_ckpt_path) src_ckpt_path="$2"; shift ;;
        -dc|--dst_ckpt_path) dst_ckpt_path="$2"; shift ;;
        -f|--function) function="$2"; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done


start_time=$(date +%H:%M:%S)

if [ -e "./log/" ]; then
    echo "./log/ is exit"
else
    mkdir ./log/
fi


if [ -z "$function" ] || [ -z "$src_ckpt_path" ] ||  [ -z "$yaml_path" ]; then
    echo "Error: Missing function src_ckpt_path and yaml_path"
    exit 1
fi


#权重量化部分
if [ "$function" == "quant_weight" ]; then
    if [ -z "$dst_ckpt_path" ]; then
        #创建输出权重文件夹
        Dst_ckpt_path=./infer_ckpt/${precision}
    else
        Dst_ckpt_path=${dst_ckpt_path}/${precision}
    fi
    if [ -z "$infer_strategy_file" ]; then
        Infer_strategy_path=./infer_strategy/${precision}
    else
        Infer_strategy_path=${infer_strategy_file}/${precision}
    fi
    # 检查是否是相同卡数
    dir_count=$(find  "$src_ckpt_path"  -mindepth 1 -maxdepth 1 -type d | wc -l)
    echo "Number of directories in '$src_ckpt_path' is: $dir_count"
    rank_num=$dir_count

    if [ "$precision" == "w8a16" ]; then
        #1. 转换成rank_num的w8a16权重
        echo "----- Start to convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        msrun --worker_num=$rank_num --local_worker_num=$rank_num --master_port=8126 \
        --log_dir=./log/msrun_log_${precision}_${rank_num}_ckpt --join=True --cluster_time_out=300 \
        python quant_ckpt.py \
        -c $yaml_path \
        -q ptq \
        -t $dataset_name \
        -s $dataset_path \
        -w int8 \
        -a None \
        -k None \
        -o None \
        -b lm_head \
        -lc $src_ckpt_path  \
        -od ${Dst_ckpt_path}_${rank_num}p \
        -ws $rank_num \
        > ./log/log_fp16_to_${precision}_${rank_num}.log 2>&1
        if find "${Dst_ckpt_path}_${rank_num}p/rank_0/" -type f -name "*.ckpt" | read; then
            echo "----- End convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        else
            echo "QUANT ERROR"
            exit 1
        fi
    elif [ "$precision" == "w8a8" ]; then
        #1. 转换成rank_num的w8a8权重
        echo "----- Start to convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        msrun --worker_num=$rank_num --local_worker_num=$rank_num --master_port=8126 \
        --log_dir=./log/msrun_log_${precision}_${rank_num}_ckpt --join=True --cluster_time_out=300 \
        python quant_ckpt.py \
        -c $yaml_path \
        -q ptq \
        -t $dataset_name \
        -s $dataset_path \
        -w int8 \
        -a int8 \
        -k None \
        -o smooth \
        -b lm_head \
        -lc $src_ckpt_path  \
        -od ${Dst_ckpt_path}_${rank_num}p \
        -ws $rank_num \
        > ./log/log_fp16_to_${precision}_${rank_num}.log 2>&1
        if find "${Dst_ckpt_path}_${rank_num}p/rank_0/" -type f -name "*.ckpt" | read; then
            echo "----- End convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        else
            echo "QUANT ERROR"
            exit 1
        fi
    elif [ "$precision" == "w8a16c8" ]; then
        #1. 转换成rank_num的w8a16c8权重
        echo "----- Start to convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        msrun --worker_num=$rank_num --local_worker_num=$rank_num --master_port=8126 \
        --log_dir=./log/msrun_log_${precision}_${rank_num}_ckpt --join=True --cluster_time_out=300 \
        python quant_ckpt.py \
        -c $yaml_path \
        -q ptq \
        -t $dataset_name \
        -s $dataset_path \
        -w int8 \
        -a None \
        -k int8 \
        -o None \
        -b lm_head \
        -lc $src_ckpt_path  \
        -od ${Dst_ckpt_path}_${rank_num}p \
        -ws $rank_num \
        > ./log/log_fp16_to_${precision}_${rank_num}.log 2>&1
        if find "${Dst_ckpt_path}_${rank_num}p/rank_0/" -type f -name "*.ckpt" | read; then
            echo "----- End convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        else
            echo "QUANT ERROR"
            exit 1
        fi
    elif [ "$precision" == "w8a8c8" ]; then
        #1. 转换成rank_num的w8a8c8权重
        echo "----- Start to convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        msrun --worker_num=$rank_num --local_worker_num=$rank_num --master_port=8126 \
        --log_dir=./log/msrun_log_${precision}_${rank_num}_ckpt --join=True --cluster_time_out=300 \
        python quant_ckpt.py \
        -c $yaml_path \
        -q ptq \
        -t $dataset_name \
        -s $dataset_path \
        -w int8 \
        -a int8 \
        -k int8 \
        -o smooth \
        -b lm_head \
        -lc $src_ckpt_path  \
        -od ${Dst_ckpt_path}_${rank_num}p \
        -ws $rank_num \
        > ./log/log_fp16_to_${precision}_${rank_num}.log 2>&1
        if find "${Dst_ckpt_path}_${rank_num}p/rank_0/" -type f -name "*.ckpt" | read; then
            echo "----- End convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        else
            echo "QUANT ERROR"
            exit 1
        fi
    elif [ "$precision" == "fp16c8" ]; then
        #1. 转换成rank_num的fp16c8权重
        echo "----- Start to convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        msrun --worker_num=$rank_num --local_worker_num=$rank_num --master_port=8126 \
        --log_dir=./log/msrun_log_${precision}_${rank_num}_ckpt --join=True --cluster_time_out=300 \
        python quant_ckpt.py \
        -c $yaml_path \
        -q ptq \
        -t $dataset_name \
        -s $dataset_path \
        -w None \
        -a None \
        -k int8 \
        -o None \
        -b None \
        -lc $src_ckpt_path  \
        -od ${Dst_ckpt_path}_${rank_num}p \
        -ws $rank_num \
        > ./log/log_fp16_to_${precision}_${rank_num}.log 2>&1
        if find "${Dst_ckpt_path}_${rank_num}p/rank_0/" -type f -name "*.ckpt" | read; then
            echo "----- End convert ${rank_num}p ${precision} weights time: $(date +%H:%M:%S) -----"
        else
            echo "QUANT ERROR"
            exit 1
        fi
    else
        echo "Wrong precision input"
        exit 1
    fi
elif [ "$function" == "qkv" ]; then
    if [ -z "$dst_ckpt_path" ]; then
    #创建输出权重文件夹
    Dst_ckpt_path=./qkv_concat_ckpt/
    else
        Dst_ckpt_path=${dst_ckpt_path}
    fi
    # 检查卡数
    dir_count=$(find  "$src_ckpt_path"  -mindepth 1 -maxdepth 1 -type d | wc -l)
    echo "Number of directories in '$src_ckpt_path' is: $dir_count"
    rank_num=$dir_count
    
    python convert_qkv_ffn.py \
    --world_size=$rank_num \
    --src_ckpt_path=$src_ckpt_path \
    --dst_ckpt_path=$Dst_ckpt_path \
    > ./log/log_convert_qkv_ffn.log 2>&1
fi
echo "Convert finish!"
end_time=$(date +%H:%M:%S)
echo "Total Start Time: $start_time, Total End Time: $end_time"
