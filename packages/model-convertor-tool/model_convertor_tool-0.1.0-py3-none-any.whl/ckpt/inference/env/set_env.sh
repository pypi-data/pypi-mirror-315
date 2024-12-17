#!/bin/bash

# help information
print_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "--convert_path           该项目代码所在的绝对路径"
    echo "--quant_conda_path       推理权重转换的conda环境所在绝对路径"
}

# parser args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --convert_path) convert_path="$2"; shift ;;
        --quant_conda_path) quant_conda_path="$2"; shift ;;
        -h|--help) print_usage; ;;
        *) echo "Unknown option: $1"; print_usage; ;;
    esac
    shift
done

if [ -z "$convert_path" ] || [ -z "$quant_conda_path" ]; then
    echo "Error: Missing convert_path and quant_conda_path required options."
else
    #设置绝对路径
    export CONVERT_PATH=$convert_path
    export QUANT_CONDA_PATH=$quant_conda_path

    echo "项目所在绝对路径: $CONVERT_PATH"
    echo "conda环境所在绝对路径: $CONVERT_PATH"
    echo "请确保CANN环境安装配置在/usr/local/Ascend/路径下"

    if [ -f /usr/local/Ascend/ascend-toolkit/set_env.sh ]; then
        source /usr/local/Ascend/ascend-toolkit/set_env.sh
        echo "已完成CANN环境配置"
    else
        echo "ascend-toolkit 未安装在默认路径，请自行完成CANN环境配置。"
    fi

    export MS_ENABLE_INTERNAL_KERNELS=on
    export MS_ENABLE_INTERNAL_BOOST=on
    export MS_ENABLE_TRACE_MEMORY=on
    export RUN_MODE=predict
    export MS_ENABLE_LCCL=on
     #export HCCL_OP_EXPANSION_MODE=AIV
    export MS_SCHED_HOST=127.0.0.1
    export MS_SCHED_PORT=2041
    export MS_SUBMODULE_LOG_v="{DISTRIBUTED:3}"
    export MS_COMPILER_CACHE_ENABLE=0
    #export MS_COMPILER_CACHE_PATH="/home/compile_cache"
    export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
    export LD_LIBRARY_PATH=/lib/aarch64-linux-gnu/:$QUANT_CONDA_PATH/lib:$LD_LIBRARY_PATH
    export LD_PRELOAD=$QUANT_CONDA_PATH/lib/libgomp.so.1:$LD_PRELOAD
    export LD_PRELOAD=$QUANT_CONDA_PATH/lib/python3.10/site-packages/torch/lib/../../torch.libs/libgomp-6e1a1d1b.so.1.0.0:$LD_PRELOAD
    export MS_INTERNAL_DISABLE_CUSTOM_KERNEL_LIST=MatMulAllReduce
    #执行修改yaml脚本中tokenizer路径命令
    python $convert_path/model/llama2_7b/trans_yaml.py
fi