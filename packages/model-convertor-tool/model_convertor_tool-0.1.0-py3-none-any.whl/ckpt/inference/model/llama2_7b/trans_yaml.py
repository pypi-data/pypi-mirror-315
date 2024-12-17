import os
import yaml

# 确保环境变量已设置
if 'CONVERT_PATH' not in os.environ:
    raise ValueError("环境变量 CONVERT_PATH 未设置")
# 获取环境变量的值
base_path = os.environ['CONVERT_PATH']

llama_tokenizer_path = f'{base_path}/model/llama2_7b/tokenizer.model'
print(f"the tokenizer_path in {llama_tokenizer_path}")

yaml_path = f'{base_path}/model/llama2_7b/quant'
print(f"the yaml_path in {yaml_path}")

# 读取YAML文件
for root, dirs, files in os.walk(yaml_path):
    for file in files:
        # 如果文件以.yaml结尾
        if file.endswith('.yaml'):
            file_path = os.path.join(root, file)

            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
            #替换tokenizer文件路径
            vocab_file_key = 'processor.tokenizer.vocab_file'
            config[vocab_file_key.split('.')[0]][vocab_file_key.split('.')[1]][vocab_file_key.split('.')[2]] = llama_tokenizer_path
            print(f"the yaml file : {file_path} has changed the tokenizer path")

            # 保存修改后的YAML文件
            with open(file_path, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
