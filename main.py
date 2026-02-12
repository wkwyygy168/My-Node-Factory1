import requests
import base64
import re

def factory_run():
    # 你的 Gist 原始数据地址
    gist_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    try:
        content = requests.get(gist_url).text
        # 1. 抓取链接类 (91个及其套娃)
        all_links = re.findall(r'[a-zA-Z0-9]+://[^\s<>"\',;]+', content)
        
        # 2. 抓取 YAML 散装类 (31个)
        yaml_blocks = re.findall(r'-\s*name:.*?\n\s+type:', content, re.DOTALL)
        
        # 3. 汇总去重并保存 (这里你可以加入 IP 去重逻辑)
        final_nodes = list(set(all_links)) # 示例：仅链接去重
        
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_nodes))
        print(f"Success! Processed {len(final_nodes) + len(yaml_blocks)} potential nodes.")
    except:
        print("Fetch failed")

if __name__ == "__main__":
    factory_run()
