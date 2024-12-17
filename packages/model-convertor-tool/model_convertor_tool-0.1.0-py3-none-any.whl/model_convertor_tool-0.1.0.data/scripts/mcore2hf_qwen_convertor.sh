set -e

export CUDA_DEVICE_MAX_CONNECTIONS=1
export CUDA_VISIBLE_DEVICES=0
PACKAGE_NAME="model_convertor_tool"
PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
MEGATRON_PATCH_PATH=$PACKAGE_PATH/ckpt/megatron-core
MEGATRON_PATH=${MEGATRON_PATCH_PATH}/Megatron-LM
export PYTHONPATH=${MEGATRON_PATH}:${MEGATRON_PATCH_PATH}:$PYTHONPATH

MASTER_ADDR=localhost
MASTER_PORT=${1}
MODEL_SIZE=${2}
HF_CKPT_PATH=${3}
SOURCE_CKPT_PATH=${4}
TARGET_CKPT_PATH=${5}
TP=${6}
PP=${7}

DISTRIBUTED_ARGS="--nproc_per_node 1 --nnodes 1 --node_rank 0 --master_addr $MASTER_ADDR --master_port $MASTER_PORT"
NUM_LAYERS=32
HIDDEN_SIZE=4096
NUM_ATTN_HEADS=32
INTERMEDIATE_SIZE=11008
EXTRA_VOCAB_SIZE=85
gqa_options=""
cpu_options=""
mg2hf=true

if [ $mg2hf = true ]; then
    convert_options="
                --convert_checkpoint_from_megatron_to_transformers
    "
elif [ $mg2hf = false ]; then
    convert_options=""
fi

torchrun ${DISTRIBUTED_ARGS} $PACKAGE_PATH/ckpt/megatron-core/toolkits/model_checkpoints_convertor/qwen_core/hf2mcore_qwen.py \
    --load ${SOURCE_CKPT_PATH} \
    --save ${TARGET_CKPT_PATH} \
    --tokenizer-model ${HF_CKPT_PATH} \
    --target-tensor-model-parallel-size ${TP} \
    --pipeline-model-parallel-size ${PP} \
    --micro-batch-size 1 \
    --save-interval 1 \
    --fp16 \
    --swiglu \
    --norm-epsilon 1e-6 \
    --num-layers ${NUM_LAYERS} \
    --hidden-size ${HIDDEN_SIZE} \
    --ffn-hidden-size ${INTERMEDIATE_SIZE} \
    --num-attention-heads ${NUM_ATTN_HEADS} \
    --max-position-embeddings 1 \
    --seq-length 1 \
    --no-async-tensor-model-parallel-allreduce \
    --patch-tokenizer-type Qwen1Tokenizer \
    --extra-vocab-size ${EXTRA_VOCAB_SIZE} \
    --untie-embeddings-and-output-weights \
    --no-rope-fusion \
    --use-rotary-position-embeddings \
    --transformer-impl transformer_engine \
    --disable-bias-linear \
    --normalization RMSNorm \
    --add-qkv-bias \
    --use-mcore-models \
    --attention-dropout 0.0 \
    --hidden-dropout 0.0 \
    ${convert_options} \
    ${gqa_options} \
    ${cpu_options}

# ELAPSED_TIME=$(($SECONDS - $START_TIME))
# echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"
