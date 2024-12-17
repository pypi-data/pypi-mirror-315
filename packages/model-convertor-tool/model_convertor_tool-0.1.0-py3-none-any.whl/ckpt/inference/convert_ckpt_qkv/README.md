# 推理权重转换

## 入参说明

| 名称              | 缩写            | 参数说明                                                                                                                         | 是否必须          |
|-----------------|---------------|------------------------------------------------------------------------------------------------------------------------------|---------------|
| --function      | -f            | Choose the function you need from the following options: train_to_infer, quant_weight, distributed_weight_transfer, pt_to_ms | 是             |
| --precision     | -p            | Set precision (fp16)                                                                                                         | 是             |
| --world_size    | -w            | Set the world size for distributed training (2, 4 or 8)                                                                      | 是             |
| --yaml_path     | -y            | Yaml path or model config path                                                                                               | 是             |
| --src_ckpt_path | -sc           | Source ckpt path                                                                                                             | 是             |
| --dst_ckpt_path | -dc           | Destination ckpt path                                                                                                        | 否             |

## 模型适配列表
| 模型        | 1-n      | n-m       | n-1      | n-16     | 16-m     |
|-----------|----------|-----------|----------|----------|----------|
| llama2-7b | &#x2714; | &#x2714;  | &#x2714; | &#x2714; | &#x2716; |


### 带qkv融合权重转换示例

#### 1.1.1 1 to n样例

```shell
# 1卡(qkv)转4卡(qkv)
yaml_path=../model/llama2_7b/qkv/llama2_7b_4p.yaml
src_ckpt_path=/workspace/ckpt/1_llama-2-7b_qkv
dst_ckpt_path=/workspace/ckpt/4_llama-2-7b
infer_strategy_file=/workspace/strategy/4_llama-2-7b
word_size=4

mkdir -p $infer_strategy_file
mkdir -p $dst_ckpt_path

bash ckpt_convert.sh \
-f distributed_weight_transfer \
-p fp16 \
-w $word_size \
-is $infer_strategy_file \
-sc $src_ckpt_path \
-dc $dst_ckpt_path \
-y $yaml_path &
```
##### 简化
```shell
# 生成权重默认保存相对路径下
# 默认路径为：
#dst_ckpt_path=../ckpt/llama2_7b/qkv/${word_size}_llama-2-7b
#infer_strategy_file=../strategy/llama2_7b/qkv/${word_size}_llama-2-7b
# word_size 转出卡数
# src_ckpt_path 转换原权重
word_size=4
src_ckpt_path=/workspace/ckpt/1_llama-2-7b_qkv

python ckpt_convert_n_to_m.sh \
-w $word_size \
-sc $src_ckpt_path &
```

#### 1.1.2 n to m样例

```shell
# 4卡(qkv)转8卡(qkv)
yaml_path=../model/llama2_7b/qkv/llama2_7b_8p.yaml
src_ckpt_path=/workspace/ckpt/4_llama-2-7b/fp16_4p_qkv
dst_ckpt_path=/workspace/ckpt/8_llama-2-7b
infer_strategy_file=/workspace/strategy/8_llama-2-7b
word_size=8

mkdir -p $infer_strategy_file
mkdir -p $dst_ckpt_path

bash ckpt_convert.sh \
-f distributed_weight_transfer \
-p fp16 \
-w $word_size \
-is $infer_strategy_file \
-sc $src_ckpt_path \
-dc $dst_ckpt_path \
-y $yaml_path &
```
##### 简化
```shell
# 生成权重默认保存相对路径下
# 默认路径为：
#dst_ckpt_path=../ckpt/llama2_7b/qkv/${word_size}_llama-2-7b
#infer_strategy_file=../strategy/llama2_7b/qkv/${word_size}_llama-2-7b
# word_size 转出卡数
# src_ckpt_path 转换原权重
word_size=8
src_ckpt_path=/workspace/ckpt/4_llama-2-7b/fp16_4p_qkv

python ckpt_convert_n_to_m.sh \
-w $word_size \
-sc $src_ckpt_path &
```


#### 1.1.3 n to m多机样例

##### 初始化多机环境
```shell
#初始化多机环境
source ../env/set_2n_env.sh

###
export MS_ENABLE_LCCL=off
# 根据多机环境修改hccl_2n_16p.json脚本
export RANKTABLEFILE='./hccl_2n_16p.json'
export MS_SCHED_HOST='10.208.200.63' # (两机中的一个ip，两机设置保持一致)
export MS_SCHED_PORT=8334 # (两机设置保持一致)
###
```
##### 转换执行
```shell
# 8卡(qkv)转16卡(qkv)
# fp16 fp16-8p 转 fp16-16p
yaml_path=../model/llama2_7b/qkv/llama2_7b_16p.yaml
src_ckpt_path=/workspace/ckpt/8_llama-2-7b/fp16_8p_qkv
dst_ckpt_path=/workspace/ckpt/16_llama-2-7b
infer_strategy_file=/workspace/strategy/16_llama-2-7b
word_size=16

mkdir -p $infer_strategy_file
mkdir -p $dst_ckpt_path

# 两台机器同时执行同一个脚本
bash ckpt_convert_for_16p.sh \
-f distributed_weight_transfer \
-p fp16 \
-w $word_size \
-is $infer_strategy_file \
-sc $src_ckpt_path \
-dc $dst_ckpt_path \
-y $yaml_path
```
##### 简化
```shell
# 生成权重默认保存相对路径下
# 默认路径为：
#dst_ckpt_path=../ckpt/llama2_7b/qkv/${word_size}_llama-2-7b
#infer_strategy_file=../strategy/llama2_7b/qkv/${word_size}_llama-2-7b
# word_size 转出卡数
# src_ckpt_path 转换原权重

# 两台机器同时执行同一个脚本
word_size=16
src_ckpt_path=/workspace/ckpt/8_llama-2-7b/fp16_8p_qkv

python ckpt_convert_n_to_m.sh \
-w $word_size \
-sc $src_ckpt_path &
```






