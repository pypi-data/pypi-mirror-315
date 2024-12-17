set -e
#检查输入参数数量
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <INPUT_PATH> <OUTPUT_PATH> <LAYERS>"
    exit 1
fi
# 获取输入参数
INPUT_PATH=$1
OUTPUT_PATH=$2
LAYERS=$3
# 执行命令
PACKAGE_NAME="model_convertor_tool"
PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
MEGATRON_PATCH_PATH=$PACKAGE_PATH/ckpt/mindformers
MEGATRON_PATH=${MEGATRON_PATCH_PATH}/mindformers
export PYTHONPATH=${MEGATRON_PATH}:${MEGATRON_PATCH_PATH}:$PYTHONPATH
python $PACKAGE_PATH/ckpt/mindformers/mindformers/models/gpt2/convert_weight.py \
    --layers $LAYERS\
    --torch_path $INPUT_PATH \
    --mindspore_path $OUTPUT_PATH