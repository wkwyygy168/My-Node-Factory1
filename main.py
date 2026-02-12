import requests
import base64
import re

def move_house():
    yaml_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    b64_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    
    try:
        # 1. 获取 all.yaml
        yaml_content = requests.get(yaml_url, timeout=15).text
        
        # 2. 获取并解码 base64.txt
        b64_res = requests.get(b64_url, timeout=15).text.strip()
        b64_res += "=" * (-len(b64_res) % 4)
        decoded = base64.b64decode(b64_res).decode('utf-8', errors='ignore')
        
        # 3. 提取链接并转换成 Clash 支持的“- 链接”格式
        extra_links = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', decoded, re.I)
        
        # 将每个链接处理成严格缩进的 YAML 列表项
        formatted_links = [f"  - {link}" for link in extra_links]
        new_nodes_block = "\n".join(formatted_links)

        # 4. 精准插入逻辑
        if "proxies:" in yaml_content:
            # 在 proxies: 这一行后面直接插入新节点，确保它们属于 proxies 列表
            final_output = yaml_content.replace("proxies:", f"proxies:\n{new_nodes_block}")
        else:
            # 如果原文件没 proxies 标记，就硬塞一个（保底）
            final_output = f"proxies:\n{new_nodes_block}\n" + yaml_content

        # 5. 保存并覆盖
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(final_output)
            
        print(f"✅ 转换镜像成功！已将 {len(extra_links)} 个节点安全并入 YAML。")
        
    except Exception as e:
        print(f"❌ 镜像失败: {e}")

if __name__ == "__main__":
    move_house()
