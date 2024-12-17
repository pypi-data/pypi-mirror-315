#!/bin/bash

# help information
print_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -p,  --precision              Set precision (fp16, w8a16, w8a8, w8a16c8, w8a8c8, fp16c8)"
    echo "  -w,  --world_size             Set the world size for distributed training (1, 2, 4 or 8)"
    echo "  -qkv,  --is_qkv_concat        Whether is the weight after qkv_concat  "
    echo "  -sc,  --src_ckpt_path         Source ckpt path"
    echo "  -dc,  --dst_ckpt_path         Destination ckpt path"
    echo "  -h,  --help                   Print this help message"
}

# parser args
while [[ "$#" -gt 0 ]]; do
    case $1 in
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

# 传参校验
if [ -z "$precision" ] || [ -z "$world_size" ] ||  [ -z "$is_qkv_concat" ] ||  [ -z "$src_ckpt_path" ] ||  [ -z "$dst_ckpt_path" ]; then
    echo "Error: Missing precision, world_size, is_qkv_concat, src_ckpt_path and dst_ckpt_path"
    exit 1
fi

# 输出路径处理
if [[ $dst_ckpt_path == */ ]]; then
  dst_ckpt_path=${dst_ckpt_path%*/}
fi

if [ ! -e $dst_ckpt_path ]; then
    mkdir -p $dst_ckpt_path
    echo "已创建目标路径：$dst_ckpt_path"
fi


#非qkv融合的1/2/4/8卡切分权重，w8a16量化
if [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a16" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a16.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a None \
    -k None \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a16" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a16.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a16" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a16.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a16" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a16.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi

#进行qkv融合后的1/2/4/8卡切分权重，w8a16量化
if [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a16" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a16_qkv.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a None \
    -k None \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1
elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a16" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a16_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a16" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a16_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a16" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a16_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi

#非qkv融合的1/2/4/8卡切分权重，w8a8量化
if [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a8" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a8.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a int8 \
    -k None \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi

#进行qkv融合后的1/2/4/8卡切分权重，w8a8量化
if [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a8" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a8_qkv.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a int8 \
    -k None \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1
elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi

#非qkv融合的1/2/4/8卡切分权重，w8a16c8量化
if [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a16c8" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a16c8.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a None \
    -k int8 \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a16c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a16c8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a16c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a16c8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a16c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a16c8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi

#进行qkv融合后的1/2/4/8卡切分权重，w8a16c8量化
if [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a16c8" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a16c8_qkv.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a None \
    -k int8 \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a16c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a16c8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a16c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a16c8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a16c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a16c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a16c8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi
#非qkv融合的1/2/4/8卡切分权重，w8a8c8量化
if [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a8c8" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a8c8.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a int8 \
    -k int8 \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a8c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a8c8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a8c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a8c8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "false" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a8c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a8c8.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi
#进行qkv融合后的1/2/4/8卡切分权重，w8a8c8量化
if [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "1" ] && [ "$precision" == "w8a8c8" ]; then
    if [[ ! $src_ckpt_path =~ \.ckpt$ ]]; then
    echo "输入路径为需为以 .ckpt 结尾的完整单卡权重路径，请重新输入"
    exit 1
    fi
    python quant_ckpt.py \
    -c $CONVERT_PATH/model/llama2_7b/quant/1_w8a8c8_qkv.yaml \
    -q ptq \
    -t boolq \
    -s $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl  \
    -w int8 \
    -a int8 \
    -k int8 \
    -o smooth \
    -b lm_head \
    -lc $src_ckpt_path \
    -od $dst_ckpt_path \
    -ws 1

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "2" ] && [ "$precision" == "w8a8c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/2_w8a8c8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "4" ] && [ "$precision" == "w8a8c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/4_w8a8c8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl

elif [ "$is_qkv_concat" == "true" ] && [ "$world_size" == "8" ] && [ "$precision" == "w8a8c8" ]; then
    rank_dirs=$(find "$src_ckpt_path" -maxdepth 1 -type d -name 'rank_*' 2>/dev/null)
    if [ -z "$rank_dirs" ]; then
        echo "输入路径格式需为 rank_*/ *.ckpt 的上一级目录"
        exit 1
    fi
    bash quant_ckpt.sh \
    -f quant_weight \
    -p w8a8c8 \
    -y $CONVERT_PATH/model/llama2_7b/quant/8_w8a8c8_qkv.yaml \
    -sc $src_ckpt_path \
    -dc $dst_ckpt_path \
    -d boolq \
    -dp $CONVERT_PATH/convert_ckpt_quant/dataset/boolq.jsonl
fi
