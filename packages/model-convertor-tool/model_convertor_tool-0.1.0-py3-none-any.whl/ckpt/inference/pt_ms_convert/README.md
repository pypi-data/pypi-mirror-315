## ckpt -> safetensor

### 参数说明

-f,  --function：输入格式为 bin2ckpt、ckpt2sft 或者 ckpt2pth

-sc,  --src_ckpt_path：输入权重所在路径

* 当function为bin2ckpt时，输入权重为huggingface下载的权重目录所在路径
* 当function为ckpt2pth时，输入权重路径需要 *.ckpt 结尾的完整权重路径，如 path/llama2_7b.ckpt
* 当function为ckpt2sft时，输入权重路径需要 *.ckpt 结尾的完整权重路径，如 path/llama2_7b.ckpt

-dc,  --dst_ckpt_path：目标权重路径



### 使用案例

```bash
#bin格式转ckpt格式
source pt_ms_convert.sh \
-f bin2ckpt \
-sc /checkpoint_huggingface/llama2_7b/ \
-dc /checkpoint_huggingface/llama2_7b_bin2ckpt

#ckpt格式转pth格式
source pt_ms_convert.sh \
-f ckpt2pth \
-sc /checkpoint_huggingface/llama2_7b_bin2ckpt/llama2_7b.ckpt \
-dc /checkpoint_huggingface/llama2_ckpt2bin

#ckpt格式转safetensor格式
source pt_ms_convert.sh \
-f ckpt2sft \
-sc /checkpoint_huggingface/llama2_7b_bin2ckpt/llama2_7b.ckpt \
-dc /checkpoint_huggingface/llama2_7b_ckpt2sft
```

