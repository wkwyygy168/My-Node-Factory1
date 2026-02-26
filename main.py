import requests
import base64
import re

def universal_mirror_factory():
    # 你的核心源列表（已修正中文逗号，并整理）
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
    seen_nodes = set()  # 用于去重的指纹库
    
    for url in sources:
        try:
            print(f"🚀 正在处理源: {url}")
            response = requests.get(url, timeout=15)
            content = response.text.strip()
            
            # --- 逻辑 A: 处理 YAML (Clash 格式) ---
            if url.endswith(".yaml") or "clash" in url.lower():
                if "proxies:" in content:
                    proxy_part = content.split("proxies:")[1]
                    # 简单的 YAML 节点提取逻辑（按行）
                    for line in proxy_part.splitlines():
                        if "server:" in line and "port:" in line:
                            # 提取服务器和端口作为指纹
                            fp = re.findall(r'server:\s*([^\s,]+).*port:\s*(\d+)', line)
                            if fp and fp[0] not in seen_nodes:
                                seen_nodes.add(fp[0])
                                yaml_results.append(line)
                        elif "-" in line and "{" in line: # 处理紧凑格式
                            yaml_results.append(line)
                else:
                    yaml_results.append(content)
            
            # --- 逻辑 B: 处理 TXT (明文/Base64) ---
            else:
                # 尝试 Base64 解码
                try:
                    padding = len(content) % 4
                    if padding: content += "=" * (4 - padding)
                    decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                    raw_links = decoded if "://" in decoded else content
                except:
                    raw_links = content
                
                # 提取链接并去重
                for line in raw_links.splitlines():
                    line = line.strip()
                    if "://" in line:
                        # 提取链接核心部分（去掉别名）进行去重
                        core_link = line.split('#')[0] if '#' in line else line
                        if core_link not in seen_nodes:
                            seen_nodes.add(core_link)
                            txt_results.append(line)
                    
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
        
    print(f"✨ 镜像大功告成！已自动过滤重复节点。")

if __name__ == "__main__":
    universal_mirror_factory()
