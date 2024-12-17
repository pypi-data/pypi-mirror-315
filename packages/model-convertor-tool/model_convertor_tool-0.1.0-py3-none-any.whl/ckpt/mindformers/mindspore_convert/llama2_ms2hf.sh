set -e 
# 检查输入参数数量 
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <INPUT_PATH> <OUTPUT_PATH>"
    exit 1
fi
# 获取输入参数
INPUT_PATH=$1
OUTPUT_PATH=$2
PACKAGE_NAME="model_convertor_tool"
PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
python $PACKAGE_PATH/ckpt/mindformers/convert_weight.py \
    --reversed \
    --model llama \
    --input_path $INPUT_PATH \
    --output_path $OUTPUT_PATH