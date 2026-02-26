import requests
import base64
import re
import yaml  # 补上可能需要的库

def universal_mirror_factory():
    # 你的核心源列表（已修正中文逗号错误）
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt",
        "https://raw.githubusercontent.com/v820965095/E-V2ray-Singbox-Clash/main/V2ray_all",
        "https://raw.githubusercontent.com/tugezhe/v2ray/main/v2ray.txt",
        "https://raw.githubusercontent.com/wzdnzd/aggregator/main/subscribe/proxy.txt",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data2025.txt",
        "https://raw.githubusercontent.com/free18/v2ray/main/v.txt",
        "https://raw.githubusercontent.com/free18/v2ray/main/c.yaml",
        "https://raw.githubusercontent.com/zipvpn/FreeVPNNodes/main/free_v2ray_xray_nodes.txt",
        "https://raw.githubusercontent.com/zipvpn/FreeVPNNodes/main/free_clash_nodes.yaml",
        "https://raw.githubusercontent.com/Flikify/Free-Node/main/v2ray.txt",
        "https://raw.githubusercontent.com/Flikify/Free-Node/main/clash.yaml",
        "https://raw.githubusercontent.com/Pawpieee/Free-Nodes/main/node.txt",
        "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml"
    ]
    
    yaml_results = []
    txt_results = []
    
    for url in sources:
        try:
            print(f"🚀 正在处理源: {url}")
            response = requests.get(url, timeout=15)
            content = response.text.strip()
            
            # --- 逻辑 A: 处理 YAML 后缀 (Clash 格式) ---
            if url.endswith(".yaml"):
                if "proxies:" in content:
                    proxy_part = content.split("proxies:")[1]
                    yaml_results.append(proxy_part)
                else:
                    yaml_results.append(content)
            
            # --- 逻辑 B: 处理 TXT 后缀 (明文/Base64 格式) ---
            else:
                try:
                    temp_content = content + "=" * (-len(content) % 4)
                    decoded = base64.b64decode(temp_content).decode('utf-8', errors='ignore')
                    if "://" in decoded:
                        txt_results.append(decoded)
                    else:
                        txt_results.append(content)
                except:
                    txt_results.append(content)
                    
        except Exception as e:
            print(f"❌ 处理 {url} 失败: {e}")

    # --- 最终产出：YAML 镜像 ---
    final_yaml = "proxies:\n" + "\n".join(yaml_results)
    with open("nodes.yaml", "w", encoding="utf-8") as f:
        f.write(final_yaml)

    # --- 最终产出：TXT 镜像 ---
    final_txt = "\n".join(txt_results)
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(final_txt)
        
    print(f"✨ 镜像大功告成！YAML 镜像已生成，TXT 镜像已生成。")

if __name__ == "__main__":
    universal_mirror_factory()
