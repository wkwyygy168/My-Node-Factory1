import requests
import re
import base64

def mega_mirror():
    # 1. 你的镜像源清单
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    ]
    
    all_nodes = []
    
    for url in sources:
        try:
            print(f"🚀 正在收割: {url}")
            # 增加超时和 UA，模拟浏览器访问
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            raw_text = response.text
            
            # --- 核心逻辑 A：暴力提取所有标准链接 ---
            # 匹配 vmess, vless, ss, ssr, trojan, hy2 等
            links = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|socks)://[^\s<>"\',;]+', raw_text, re.I)
            
            for link in links:
                if "vmess://" in link:
                    try:
                        # 自动处理 VMess 内部可能的 Base64 编码
                        b64_part = link.split("vmess://")[1].strip()
                        b64_part += "=" * (-len(b64_part) % 4)
                        decoded = base64.b64decode(b64_part).decode('utf-8', errors='ignore')
                        # 如果解出来的东西还是链接（套娃），再次提取
                        if "://" in decoded:
                            all_nodes.extend(re.findall(r'[a-zA-Z0-9]+://[^\s<>"\',;]+', decoded))
                        else:
                            all_nodes.append(link)
                    except:
                        all_nodes.append(link)
                else:
                    all_nodes.append(link)

            # --- 核心逻辑 B：尝试对整个页面进行 Base64 解码 (针对 base64.txt) ---
            try:
                # 尝试补齐并解码
                b64_content = raw_text.strip()
                b64_content += "=" * (-len(b64_content) % 4)
                decoded_page = base64.b64decode(b64_content).decode('utf-8', errors='ignore')
                if "://" in decoded_page:
                    b64_links = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|socks)://[^\s<>"\',;]+', decoded_page, re.I)
                    all_nodes.extend(b64_links)
            except:
                pass

        except Exception as e:
            print(f"❌ 收割 {url} 出错: {e}")

    # --- 最终去重 ---
    # 彻底解决重复节点堆积问题
    unique_nodes = list(set(all_nodes))
    
    # --- 写入文件 ---
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✨ 镜像大获全胜！已成功搬运并合并 {len(unique_nodes)} 个节点到 nodes.txt")
        else:
            # 保底防止 0 bytes
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#节点加载中_请稍后刷新")
            print("⚠️ 未发现节点，已写入保底数据。")

if __name__ == "__main__":
    mega_mirror()
