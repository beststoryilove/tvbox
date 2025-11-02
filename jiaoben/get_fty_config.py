import json5, base64, requests
import hashlib, os

output_jar = "fty/jar/fty.jar"
output_config = "fty/config.json"
# 确保输出目录存在
output_dir = os.path.dirname(output_jar)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
resp = requests.get('http://www.饭太硬.net/tv', headers={'user-agent': 'okhttp/3.12.5'})
b64  = resp.text.split('**')[-1].strip()
config = base64.b64decode(b64).decode('utf-8')
cfg  = json5.loads(config)

#写config
with open(output_config, 'w', encoding='utf-8') as f:
    f.write(config)  # config 是 str
print(f'Saved  {len(config)} bytes')

header = {'user-agent': 'okhttp/3.12.5'}

# 原始 spider 串
spider = cfg['spider']

# 1. 分割
url, _, expect_md5 = spider.partition(';md5;')

# 2. 下载
print('Downloading →', url)
r = requests.get(url, headers=header, timeout=30)
r.raise_for_status()
with open(output_jar, 'wb') as f:
    f.write(r.content)
print(f'Saved  {len(r.content)} bytes')

# 3. 校验
real_md5 = hashlib.md5(r.content).hexdigest()
print('Expect :', expect_md5)
print('Actual :', real_md5)
print('Match  :', '✅' if real_md5 == expect_md5 else '❌')
