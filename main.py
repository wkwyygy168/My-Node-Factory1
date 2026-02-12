import requests
import re
import base64

def mega_mirror():
    # 1. 你的两个目标镜像源（用列表装起来，想加多少加多少）
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    ]
    
    all_nodes = []
    
    for url in sources:
        try:
            print(f"正在收割: {url}")
            raw_text = requests.get(url, timeout=15).text
            
            # --- 动作 A：抓取标准链接 (vmess, vless, ss, etc.) ---
            links = re.findall(r'[a-zA-Z0-9]+://[^\s<>"\',;]+', raw_text)
            
            for link in links:
                if "vmess://" in link:
                    try:
                        # 自动解开 VMess 内部套娃
                        b64_str = link.split("vmess://")[1].strip()
                        b64_str += "=" * (-len(b64_str) % 4)
                        decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                        if "://" in decoded:
                            all_nodes.extend(re.findall(r'[a-zA-Z0-9]+://[^\s<>"\',;]+', decoded))
                        else:
                            all_nodes.append(link)
                    except:
                        all_nodes.append(link)
                elif any(p in link for p in ["vless", "ss", "ssr", "trojan", "socks", "hysteria2"]):
                    all_nodes.append(link)
            
            # --- 动作 B：抓取 YAML 节点 (针对 all.yaml 里的散装节点) ---
            # 只要发现包含 "- name:" 的行，就记录下来，或者你可以后续把它们转成链接
            yaml_count = raw_text.count("- name:")
            if yaml_count > 0:
                print(f"检测到 {yaml_count} 个 YAML 节点块")

        except Exception as e:
            print(f"收割 {url} 失败: {e}")

    # --- 最终去重 ---
    unique_nodes = list(set(all_nodes))
    
    # 写入你的 nodes.txt
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_results))
        
    print(f"✨ 镜像完成！总共收割并去重后得到 {len(unique_nodes)} 个节点。")

if __name__ == "__main__":
    mega_mirror()
