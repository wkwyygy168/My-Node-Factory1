import requests
import base64
import yaml
import re
import socket
from concurrent.futures import ThreadPoolExecutor

def check_node_alive(node_info):
    """测试节点是否存活 (TCP 握手)"""
    try:
        if isinstance(node_info, dict):
            server, port = node_info.get('server'), int(node_info.get('port'))
        else:
            match = re.search(r'@?([^:/]+):(\d+)', node_info)
            if not match: return False
            server, port = match.group(1), int(match.group(2))
        with socket.create_connection((server, port), timeout=3):
            return True
    except:
        return False

def universal_mirror_factory():
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
    
    all_proxies, all_txt_links, seen_ips = [], [], set()

    for url in sources:
        try:
            res = requests.get(url, timeout=15)
            content = res.text
            if ".yaml" in url or "clash" in url.lower():
                data = yaml.safe_load(content)
                if isinstance(data, dict) and 'proxies' in data:
                    for p in data['proxies']:
                        fp = f"{p.get('server')}:{p.get('port')}"
                        if fp not in seen_ips:
                            seen_ips.add(fp); all_proxies.append(p)
            else:
                decoded = content
                if "://" not in content[:50]:
                    try: decoded = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
                    except: pass
                for line in decoded.splitlines():
                    if "://" in line:
                        core = line.split('#')[0]
                        if core not in seen_ips:
                            seen_ips.add(core); all_txt_links.append(line)
        except: pass

    # 写入全量文件 (nodes.*)
    with open("nodes.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"proxies": all_proxies}, f, allow_unicode=True, sort_keys=False)
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_txt_links))

    # 执行测速并写入精选文件 (fast_nodes.*)
    with ThreadPoolExecutor(max_workers=50) as ex:
        f_proxies = [p for p, a in zip(all_proxies, list(ex.map(check_node_alive, all_proxies))) if a]
        f_links = [l for l, a in zip(all_txt_links, list(ex.map(check_node_alive, all_txt_links))) if a]

    with open("fast_nodes.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"proxies": f_proxies}, f, allow_unicode=True, sort_keys=False)
    with open("fast_nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(f_links))

if __name__ == "__main__":
    universal_mirror_factory()
