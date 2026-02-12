import requests
import base64
import re

def move_house():
    target_urls = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    ]
    
    combined_nodes = []
    
    for url in target_urls:
        try:
            response = requests.get(url, timeout=15)
            raw_content = response.text
            
            # --- 关键修改：不论是明文还是乱码，我们只提取里面的节点链接 ---
            # 这样就能过滤掉 all.yaml 里的 YAML 杂质，解决 Karing 的报错
            nodes = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', raw_content, re.I)
            
            if nodes:
                combined_nodes.extend(nodes)
            else:
                # 如果没搜到链接，说明可能是纯 Base64 (针对 base64.txt)
                try:
                    missing_padding = len(raw_content.strip()) % 4
                    content = raw_content.strip() + ("=" * (4 - missing_padding) if missing_padding else "")
                    decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                    combined_nodes.extend(re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', decoded, re.I))
                except:
                    pass
        except Exception as e:
            print(f"❌ 搬运失败: {e}")

    # 汇总并去重，生成纯净的订阅文件
    unique_nodes = list(set(combined_nodes))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_nodes))
            
    print(f"✅ 镜像成功！已清理杂质并导出 {len(unique_nodes)} 个标准节点。")

if __name__ == "__main__":
    move_house()
