# 量化功能使用说明

### 功能说明

* llama2模型：支持完整权重以及2、4、8卡转换后的分布式权重，以及添加qkv融合操作后的1、2、4、8权重，进行w8a16、w8a8、w8a16c8、w8a8c8四种精度的模型权重量化
* llama3模型：适配中
* baichuan2模型：适配中

### 输入说明

执行脚本 quant.sh 进行量化，输入参数说明：

*  -p, --precision：模型量化精度，可输入w8a16、w8a8、w8a16c8、w8a8c8
* -w, --world_size：模型权重对应npu卡数，可输入1、2、4、8
* -qkv, --is_qkv_concat：是否为qkv融合后的权重
* -sc, --src_ckpt_path：原始权重所在目录
* -dc, --dst_ckpt_path：目标权重所在目录
*  -h,  --help：参数说明

补充：

-src/--src_ckpt_path参数

* 如果输入为单卡权重，输入格式需要为 ".ckpt" 结尾的权重路径，举例： -sc  /checkpoint_ckpt/llama2_7b/rank_0/llama2_7b.ckpt

* 如果输入为为多卡权重，输入格式需为 “rank_*/ *.ckpt" 的上一级目录，举例：-sc /checkpoint_ckpt/4_llama2_7b ，其中4_llama2_7b的子目录为 "rank_0/checkpoint_0.ckpt"、"rank_1/checkpoint_1.ckpt" ....

### 使用案例

```bash
#案例一：llama2_7b模型，4卡、经过qkv融合的权重，进行w8a8量化
#输入权重目录为"/checkpoint_ckpt/4_llama2_7b_qkv",输出权重路径为“/checkpoint_ckpt/4_llama2_7b_qkv_w8a8”
cd $CONVERT_PATH/convert_ckpt_quant #进入quant.sh脚本所在路径
source quant.sh \
-p w8a8 \
-w 4 \
-qkv true \
-sc /checkpoint_ckpt/4_llama2_7b_qkv \
-dc /checkpoint_ckpt/4_llama2_7b_qkv_w8a8


#案例二：llama2_7b模型，8卡、未经过qkv融合的权重，进行w8a16量化
#输入权重目录为"/checkpoint_ckpt/8_llama2_7b",输出权重路径为“/checkpoint_ckpt/8_llama2_7b_w8a16”
cd $CONVERT_PATH/convert_ckpt_quant #进入quant.sh脚本所在路径
source quant.sh \
-p w8a16 \
-w 8 \
-qkv false \
-sc /checkpoint_ckpt/8_llama2_7b \
-dc /checkpoint_ckpt/8_llama2_7b_w8a16

#案例三：llama2_7b模型，单卡，未经过qkv融合的权重，进行w8a8量化
#输入权重路径为：/checkpoint_ckpt/llama2_7b/rank_0/llama2_7b.ckpt
#输出权重路径为：/checkpoint_ckpt/llama2_7b_w8a16
cd $CONVERT_PATH/convert_ckpt_quant #进入quant.sh脚本所在路径
source quant.sh \
-p w8a8 \
-w 1 \
-qkv false \
-sc /checkpoint_ckpt/llama2_7b/rank_0/llama2_7b.ckpt \
-dc /checkpoint_ckpt/8_llama2_7b_w8a16
```

