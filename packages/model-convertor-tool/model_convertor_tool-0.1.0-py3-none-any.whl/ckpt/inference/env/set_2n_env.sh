export MS_ENABLE_LCCL=off
# 根据多机环境修改hccl_2n_16p.json脚本
export RANKTABLEFILE='./hccl_2n_16p.json'
export MS_SCHED_HOST='10.208.200.63' # (两机中的一个ip，两机设置保持一致)
export MS_SCHED_PORT=8334 # (两机设置保持一致)