### 添加qkv融合执行案例

```bash
python convert_qkv_ffn.py \
--world_size=4 \
--src_ckpt_path=/checkpoint_ckpt/4_llama2_7b \
--dst_ckpt_path=/checkpoint_ckpt/4_llama2_7b_qkv_test \
> ./log.txt 2>&1
```

word_size ：输入原始权重为几卡切分权重；
-src_ckpt_path ：输入原始权重路径；
-dst_ckpt_path ：添加qkv融合后的权重输出路径