import os
import yaml

# 确保环境变量已设置
if 'CONVERT_PATH' not in os.environ:
    raise ValueError("环境变量 CONVERT_PATH 未设置")
if 'LLAMA_TOKENIZER' not in os.environ:
    raise ValueError("环境变量 LLAMA_TOKENIZER 未设置")

# 获取环境变量的值
llama_tokenizer = os.environ['LLAMA_TOKENIZER']
base_path = os.environ['CONVERT_PATH']

print(f"base_path is {base_path}")
print(f"llama2_tokenizer_path is {llama_tokenizer}")

llama_tokenizer_path = f'"{llama_tokenizer}"'
file_path = f"{base_path}/llama2_7b/yaml/4_w8a16.yaml"


# 读取YAML文件
with open(file_path, 'r') as file:
    config = yaml.safe_load(file)


vocab_file_key = 'processor.tokenizer.vocab_file'
config[vocab_file_key.split('.')[0]][vocab_file_key.split('.')[1]][vocab_file_key.split('.')[2]] = llama_tokenizer_path

vocab_file_value = config['processor']['tokenizer']['vocab_file']
# 打印vocab_file的值
print(f"The value of vocab_file is: {vocab_file_value}")

# 保存修改后的YAML文件
with open('/load/0923/ckpt_convert/llama2_7b/yaml/4_w8a16.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

