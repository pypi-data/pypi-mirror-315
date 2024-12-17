model_convertor=${1} 
convertor_list="nv hw inference"
if ! echo "$convertor_list" | grep -Pq "$model_convertor"; then
    echo "模型转换器仅支持nv hw inference的转换,您的输入参数为: $model_convertor "
    exit 1  # 失败时返回1
fi
if [ "$model_convertor" = "nv" ]; then
    model=${2}
    hf2mcore=${3}
    MASTER_PORT=${4}
    model_size=${5}
    HG_CKPT_PATH=${6}
    SOURCE_CKPT_PATH=${7}
    TARGET_CKPT_PATH=${8}
    TP=${9}
    PP=${10}
    model_list="baichuan2 deepseek llama2 llama3 qwen qwen2 qwen1.5"

    if echo "$model_list" | grep -Pq "$model"; then
        if [ "$hf2mcore" = "true" ]; then
            model_script="hf2mcore_${model}_convertor.sh"
        else
            model_script="mcore2hf_${model}_convertor.sh"
        fi
        eval $model_script $MASTER_PORT $model_size $HG_CKPT_PATH $SOURCE_CKPT_PATH $TARGET_CKPT_PATH $TP $PP
    else
        echo "nv模型 $model 暂不支持权重转换"
        exit 1  # 失败时返回1
    fi
elif [ "$model_convertor" = "hw" ]; then
    model=${2}
    hf2ms=${3}
    INPUT_PATH=${4}
    OUTPUT_PATH=${5}
    LAYERS=${6}
    model_list="gpt2 llama2 llama3"
    if echo "$model_list" | grep -Pq "$model"; then
        if [ "$hf2ms" = "true" ]; then
            model_script="${model}_hf2ms.sh"
        else
            model_script="${model}_ms2hf.sh"
        fi
        eval $model_script $INPUT_PATH $OUTPUT_PATH $LAYERS
    else
        echo "hw模型 $model 暂不支持权重转换"
        exit 1  # 失败时返回1
    fi
elif [ "$model_convertor" = "inference" ]; then
    PACKAGE_NAME="model_convertor_tool"
    PACKAGE_PATH=$(pip show $PACKAGE_NAME | grep Location | cut -d' ' -f2)
    quant_conda_path=$CONDA_PREFIX
    source ${PACKAGE_PATH}/ckpt/inference/env/set_env.sh --convert_path ${PACKAGE_PATH}/ckpt/inference --quant_conda_path ${quant_conda_path}
    echo "set_env 执行成功"
    print_usage() {
        echo "Usage: $0 inference [options]"
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
            inference) shift; continue ;;
            -f|--function) function="$2"; shift 2 ;;
            -p|--precision) precision="$2"; shift 2 ;;
            -w|--world_size) world_size="$2"; shift 2 ;;
            -qkv|--is_qkv_concat) is_qkv_concat="$2"; shift 2 ;;
            -sc|--src_ckpt_path) src_ckpt_path="$2"; shift 2 ;;
            -dc|--dst_ckpt_path) dst_ckpt_path="$2"; shift 2 ;;
            -h|--help) print_usage; exit 0 ;;
            *) echo "Unknown option: $1"; print_usage; exit 1 ;;
        esac
    done
    echo "function: $function precision: $precision world_size: $world_size is_qkv_concat: $is_qkv_concat src_ckpt_path: $src_ckpt_path dst_ckpt_path: $dst_ckpt_path"
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
fi