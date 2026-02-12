import requests
import base64
import re

def move_house():
    # 1. 目标源清单：这就是你的“订阅源镜像”核心
    target_urls = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    ]
    
    final_nodes_list = []
    
    for url in target_urls:
        try:
            # 2. 下载内容
            response = requests.get(url, timeout=15)
            raw_content = response.text.strip()
            
            # 3. 搬运逻辑：
            # 针对 base64.txt：尝试解码
            # 针对 all.yaml：提取链接
            
            # 先尝试整体 Base64 解码 (适配 base64.txt)
            try:
                temp_content = raw_content
                missing_padding = len(temp_content) % 4
                if missing_padding:
                    temp_content += "=" * (4 - missing_padding)
                decoded_data = base64.b64decode(temp_content).decode('utf-8', errors='ignore')
                
                # 如果解出来包含协议头，说明是加密的订阅
                if "://" in decoded_data:
                    found = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', decoded_data, re.I)
                    final_nodes_list.extend(found)
                else:
                    # 如果不是加密订阅，就按明文提取 (适配 all.yaml)
                    found = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', raw_content, re.I)
                    final_nodes_list.extend(found)
            except:
                # 解码失败，直接按明文提取
                found = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', raw_content, re.I)
                final_nodes_list.extend(found)
                
        except Exception as e:
            print(f"❌ 搬运源 {url} 失败: {e}")

    # 4. 汇总存入你的仓库文件 (nodes.txt)
    # 去重后保存，确保镜像干净
    unique_nodes = list(set(final_nodes_list))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ 镜像搬运成功！共收割 {len(unique_nodes)} 个节点到你的仓库。")
        else:
            print("⚠️ 未发现有效节点内容。")

if __name__ == "__main__":
    move_house()
