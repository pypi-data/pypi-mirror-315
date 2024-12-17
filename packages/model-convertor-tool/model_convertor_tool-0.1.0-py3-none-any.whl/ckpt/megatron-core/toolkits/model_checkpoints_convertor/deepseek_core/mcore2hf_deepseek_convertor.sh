#!/bin/bash

export CUDA_VISIBLE_DEVICES=0
export CUDA_DEVICE_MAX_CONNECTIONS=1
START_TIME=$SECONDS
MASTER_ADDR=localhost
PACKAGE_NAME="model_convertor_tool"
PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
MEGATRON_PATCH_PATH=$PACKAGE_PATH/ckpt/megatron-core
MEGATRON_PATH=${MEGATRON_PATCH_PATH}/Megatron-LM
export PYTHONPATH=${MEGATRON_PATH}:${MEGATRON_PATCH_PATH}:$PYTHONPATH
MASTER_PORT=${1}
MODEL_SIZE=${2}
HG_CKPT_PATH=${3}
SOURCE_CKPT_PATH=${4}
TARGET_CKPT_PATH=${5}
TP=${6}
PP=${7}
EXTRA_VOCAB_SIZE=2400
NUM_EXPERTS=0
EXPERTS_TOPK=0
EP=0
NUM_EXPERT_SPLITS=0
mg2hf=true

if [ $MODEL_SIZE = 7B ]; then

NUM_LAYERS=30
HIDDEN_SIZE=4096
NUM_ATTN_HEADS=32
INTERMEDIATE_SIZE=11008
NUM_KV_HEADS=32
VOCAB_SIZE=102400
ROPE_THETA=10000
RMS_NORM_EPS=1e-6
gqa_options=""

fi

if [ $NUM_EXPERT_SPLITS -gt 0 ]; then

INTERMEDIATE_SIZE=$(( ${INTERMEDIATE_SIZE} / ${NUM_EXPERT_SPLITS}))

fi

if [ $NUM_EXPERTS -gt 0 ]; then
    expert_options="
                --moe-router-topk ${EXPERTS_TOPK} \
                --num-experts ${NUM_EXPERTS} \
                --expert-model-parallel-size 1 \
                --target_expert_model_parallel_size ${EP} \
                --num_expert_split_size ${NUM_EXPERT_SPLITS} \
    "
fi

if [ $mg2hf = true ]; then
    convert_options="
                --convert_checkpoint_from_megatron_to_transformers
    "
elif [ $mg2hf = false ]; then
    convert_options=""
fi

DISTRIBUTED_ARGS="--nproc_per_node 1 --nnodes 1 --node_rank 0 --master_addr $MASTER_ADDR --master_port $MASTER_PORT"

if [ $MODEL_SIZE != 70B ]; then

torchrun ${DISTRIBUTED_ARGS} $PACKAGE_PATH/ckpt/megatron-core/toolkits/model_checkpoints_convertor/deepseek_core/hf2mcore.py \
    --load_path ${SOURCE_CKPT_PATH} \
    --save_path ${TARGET_CKPT_PATH} \
    --tokenizer-model ${HG_CKPT_PATH} \
    --huggingface_model_path ${HG_CKPT_PATH} \
    --megatron-path ${MEGATRON_PATH} \
    --target_tensor_model_parallel_size ${TP} \
    --target_pipeline_model_parallel_size ${PP} \
    --micro-batch-size 1 \
    --fp16 \
    --swiglu \
    --num-layers ${NUM_LAYERS} \
    --hidden-size ${HIDDEN_SIZE} \
    --ffn-hidden-size ${INTERMEDIATE_SIZE} \
    --norm-epsilon ${RMS_NORM_EPS}\
    --num-attention-heads ${NUM_ATTN_HEADS} \
    --max-position-embeddings 4096 \
    --seq-length 1 \
    --no-async-tensor-model-parallel-allreduce \
    --patch-tokenizer-type DeepseekTokenizer \
    --extra-vocab-size ${EXTRA_VOCAB_SIZE} \
    --untie-embeddings-and-output-weights \
    --no-rope-fusion \
    --use-rotary-position-embeddings \
    --rotary-base ${ROPE_THETA} \
    --transformer-impl transformer_engine \
    --disable-bias-linear \
    --normalization RMSNorm \
    --use-mcore-models \
    --attention-dropout 0.0 \
    --hidden-dropout 0.0 \
    ${expert_options} \
    ${convert_options} \
    ${gqa_options}

else
python $PACKAGE_PATH/ckpt/megatron-core/toolkits/model_checkpoints_convertor/deepseek_core/hf2mcore.py \
  --load ${HG_CKPT_PATH} \
  --megatron-path ${MEGATRON_PATH} \
  --load_path ${SOURCE_CKPT_PATH} \
  --save_path ${TARGET_CKPT_PATH} \
  --target_params_dtype bf16 \
  --target_tensor_model_parallel_size ${TP} \
  --target_pipeline_model_parallel_size ${PP} \
  ${convert_options} \

fi

ELAPSED_TIME=$(($SECONDS - $START_TIME))
echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"
