set -e
#检查输入参数数量
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <INPUT_PATH> <OUTPUT_PATH>"
    exit 1
fi
# 获取输入参数
INPUT_PATH=$1
OUTPUT_PATH=$2
PACKAGE_NAME="model_convertor_tool"
PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
MEGATRON_PATCH_PATH=$PACKAGE_PATH/ckpt/mindformers
MEGATRON_PATH=${MEGATRON_PATCH_PATH}/mindformers
export PYTHONPATH=${MEGATRON_PATH}:${MEGATRON_PATCH_PATH}:$PYTHONPATH
python $PACKAGE_PATH/ckpt/mindformers/mindformers/models/gpt2/convert_weight.py \
    --reversed \
    --torch_path $OUTPUT_PATH \
    --mindspore_path $INPUT_PATH

# python -m ckpt.mindformers.mindspore_convert.convert_weight \
