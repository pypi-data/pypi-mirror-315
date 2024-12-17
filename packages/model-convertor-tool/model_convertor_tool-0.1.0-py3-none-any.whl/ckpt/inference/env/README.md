## 权重转换环境配置说明

### 脚本参数说明

使用 set_env.sh 完成环境变量配置，输入参数：

* --convert_path      该项目代码所在的绝对路径

* --quant_conda_path       推理权重转换的conda环境所在绝对路径

补充：需要确保用户将CANN环境安装在 /usr/local/Ascend/ 路径下

### 使用案例

```bash
cd path/ #进入脚本所在路径
source env/set_env.sh \
--convert_path /load/0923/ckpt_convert \
--quant_conda_path /root/miniconda3/envs/ckpt_convert
```

