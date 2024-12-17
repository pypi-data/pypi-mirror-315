#!/bin/bash
export CUDA_DEVICE_MAX_CONNECTIONS=1

GPUS_PER_NODE=4
MASTER_ADDR=192.168.0.14
MASTER_PORT=29501
NUM_NODES=1
NODE_RANK=0
WORLD_SIZE=$(expr $GPUS_PER_NODE \* $NUM_NODES)

tp_size=1
pp_size=1
sp_size=1
dp_size=8

jobname="LM_TP${tp_size}_PP${pp_size}_SP${sp_size}_DP${dp_size}"
TENSORBOARD_LOGS_PATH="log/tensorboard/${jobname}"
mkdir -p ${TENSORBOARD_LOGS_PATH}

CHECKPOINT_PATH="test_results/checkpoints/gpt2"
if [ -d "$CHECKPOINT_PATH" ]; then
    # 删除所有文件
    find "$CHECKPOINT_PATH" -type f -exec rm {} \;
    # 删除所有空子目录
    find "$CHECKPOINT_PATH" -type d -empty -delete
else
    echo "Path does not exist or is not a directory."
fi
mkdir -p ${CHECKPOINT_PATH}

VOCAB_FILE=data/gpt2-vocab.json
MERGE_FILE=data/gpt2-merges.txt
DATA_PATH=data/meg-gpt2-oscar-en-10k_text_document

DISTRIBUTED_ARGS=(
    --nproc_per_node $GPUS_PER_NODE 
    --nnodes $NUM_NODES 
    --master_addr $MASTER_ADDR 
    --master_port $MASTER_PORT
)

GPT_MODEL_ARGS=(
    --num-layers 32
    --hidden-size 2816
    --num-attention-heads 32
    --seq-length 2048 
    --max-position-embeddings 2048 
)

TRAINING_ARGS=(
    --micro-batch-size 2
    --global-batch-size 32
    # --rampup-batch-size 16 16 5859375 
    --train-iters 5000
    --weight-decay 0.1 
    --adam-beta1 0.9 
    --adam-beta2 0.95 
    --init-method-std 0.006 
    --clip-grad 1.0 
    --fp16
    --lr 6.0e-5 
    --lr-decay-style cosine 
    --min-lr 1.0e-5
    --lr-warmup-fraction .001 
    --lr-decay-iters 200
    --use-mcore-models
    
    --log-batch-size-to-tensorboard
    --log-timers-to-tensorboard
    --log-throughput
    --position-embedding-type rope
    --tensorboard-log-interval 20
    --use-rotary-position-embeddings
)

MODEL_PARALLEL_ARGS=(
	--tensor-model-parallel-size $tp_size
	--pipeline-model-parallel-size $pp_size
)

DATA_ARGS=(
    --data-path $DATA_PATH 
    --vocab-file $VOCAB_FILE 
    --merge-file $MERGE_FILE 
    --split 949,50,1
)

EVAL_AND_LOGGING_ARGS=(
    --log-interval 20
    --save-interval 200 
    --eval-interval 500 
    --save $CHECKPOINT_PATH 
    --load $CHECKPOINT_PATH 
    --eval-iters 10
    --profile
    --profile-ranks 0
    --tensorboard-dir $TENSORBOARD_LOGS_PATH 
)

torchrun ${DISTRIBUTED_ARGS[@]} pretrain_gpt.py \
    ${GPT_MODEL_ARGS[@]} \
    ${TRAINING_ARGS[@]} \
    ${MODEL_PARALLEL_ARGS[@]} \
    ${DATA_ARGS[@]} \
    ${EVAL_AND_LOGGING_ARGS[@]}