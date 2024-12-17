#!/bin/bash
PACKAGE_NAME="model_convertor_tool"
PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
quant_conda_path=$CONDA_PREFIX
source ${PACKAGE_PATH}/ckpt/inference/env/set_env.sh --convert_path ${PACKAGE_PATH}/ckpt/inference --quant_conda_path ${quant_conda_path}
echo "set_env 执行成功"
# help information
print_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -f,  --function               Choose funtion (quant, pt2ckpt, ckpt2sft, ckpt2pth, n2m_noqkv,n2m_qkv,add_qkv)"
    echo "  -p,  --precision              Set precision (w8a16, w8a8, w8a16c8, w8a8c8)"
    echo "  -w,  --world_size             Set the world size for distributed training (1, 2, 4 or 8)"
    echo "  -qkv,  --is_qkv_concat        Whether is the weight after qkv_concat  "
    echo "  -sc,  --src_ckpt_path         Source ckpt path"
    echo "  -dc,  --dst_ckpt_path         Destination ckpt path"
    echo "  -h,  --help                   Print this help message"
}

# parser args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--function) function="$2"; shift ;;
        -p|--precision) precision="$2"; shift ;;
        -w|--world_size) world_size="$2"; shift ;;
        -qkv|--is_qkv_concat) is_qkv_concat="$2"; shift ;;
        -sc|--src_ckpt_path) src_ckpt_path="$2"; shift ;;
        -dc|--dst_ckpt_path) dst_ckpt_path="$2"; shift ;;
        -h|--help) print_usage; exit 0 ;;
        *) echo "Unknown option: $1"; print_usage; exit 1 ;;
    esac
    shift
done

# check input is not none
if [ -z "$src_ckpt_path" ] ||  [ -z "$function" ]; then
    echo "Error: Missing function and src_ckpt_path required options."
    print_usage
    exit 1
fi

#pytorch权重和mindspore权重互转功能

if [ "$function" == "pt2ckpt" ] ; then
    cd $CONVERT_PATH/pt_ms_convert
    source pt_ms_convert.sh \
    -f bin2ckpt \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path

elif [ "$function" == "ckpt2pth" ]; then
    cd $CONVERT_PATH/pt_ms_convert
    source pt_ms_convert.sh \
    -f ckpt2pth \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path

elif [ "$function" == "ckpt2sft" ]; then
    cd $CONVERT_PATH/pt_ms_convert
    source pt_ms_convert.sh \
    -f ckpt2sft \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path

elif [ "$function" == "add_qkv" ]; then

    if [[ $dst_ckpt_path == */ ]]; then
        dst_ckpt_path=${dst_ckpt_path%*/}
    fi
    if [ ! -e $dst_ckpt_path ]; then
        mkdir -p $dst_ckpt_path
        echo "已创建目标路径：$dst_ckpt_path"
    fi

    if [[ "$src_ckpt_path" == *.ckpt ]]; then
        src_ckpt_path=$(dirname "$(dirname "$src_ckpt_path")")
    else
        echo "Error: The path does not end with .ckpt"
    fi

    cd $CONVERT_PATH/add_qkv_concat
    python convert_qkv_ffn.py \
    --world_size=$world_size \
    --src_ckpt_path=$src_ckpt_path \
    --dst_ckpt_path=$dst_ckpt_path

elif [ "$function" == "quant" ] ; then
    cd $CONVERT_PATH/convert_ckpt_quant
    source quant.sh \
    -p $precision \
    -w $world_size \
    -qkv $is_qkv_concat \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path

elif [ "$function" == "n2m_noqkv" ] ; then
    cd $CONVERT_PATH/convert_ckpt_noqkv
    source ckpt_convert_n_to_m.sh \
    --world_size_1 $world_size \
    --src_ckpt_path_1 $src_ckpt_path \
    --dst_ckpt_path_1 $dst_ckpt_path

elif [ "$function" == "n2m_qkv" ] ; then
    cd $CONVERT_PATH/convert_ckpt_qkv
    source ckpt_convert_n_to_m.sh \
    --world_size_a $world_size \
    --src_ckpt_path_a $src_ckpt_path \
    --dst_ckpt_path_a $dst_ckpt_path
else
    echo "Please enter the correct function parameters"
fi