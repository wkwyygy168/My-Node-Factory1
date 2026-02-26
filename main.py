import requests
import base64
import yaml
import re
import socket
from concurrent.futures import ThreadPoolExecutor

def check_node_alive(node_info):
    """测试节点是否存活 (TCP 握手)"""
    try:
        server = node_info.get('server')
        port = int(node_info.get('port'))
        # 3秒超时，防止阻塞
        with socket.create_connection((server, port), timeout=3):
            return True
    except:
        return False

def universal_mirror_factory():
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://raw.githubusercontent.com/Flikify/Free-Node/main/clash.yaml",
        "https://raw.githubusercontent.com/Pawpieee/Free-Nodes/main/node.txt",
        "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml"
    ]
    
    all_proxies = [] # 全量 YAML 节点
    all_txt_links = [] # 全量 TXT 链接
    seen_ips = set()

    # 1. 抓取与初步去重
    for url in sources:
        try:
            print(f"🚀 正在抓取: {url}")
            res = requests.get(url, timeout=15)
            content = res.text
            
            if ".yaml" in url or "clash" in url.lower():
                try:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict) and 'proxies' in data:
                        for p in data['proxies']:
                            fp = f"{p.get('server')}:{p.get('port')}"
                            if fp not in seen_ips:
                                seen_ips.add(fp)
                                all_proxies.append(p)
                except: pass
            else:
                decoded = content
                if "://" not in content[:50]:
                    try: decoded = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
                    except: pass
                for line in decoded.splitlines():
                    if "://" in line:
                        core = line.split('#')[0]
                        if core not in seen_ips:
                            seen_ips.add(core)
                            all_txt_links.append(line)
        except Exception as e:
            print(f"❌ 失败 {url}: {e}")

    # 2. 写入全量文件 (不测速)
    with open("nodes.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"proxies": all_proxies}, f, allow_unicode=True, sort_keys=False)
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_txt_links))

    # 3. 筛选精选版 (并发测速)
    print(f"⚡ 开始测速筛选 (总计 {len(all_proxies) + len(all_txt_links)} 节点)...")
    
    # 筛选 YAML 节点
    fast_proxies = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_node_alive, all_proxies))
        for p, is_alive in zip(all_proxies, results):
            if is_alive: fast_proxies.append(p)

    # 筛选 TXT 链接 (从链接提取 IP/端口测试)
    fast_txt_links = []
    txt_test_data = []
    for link in all_txt_links:
        match = re.search(r'@?([^:/]+):(\d+)', link)
        if match:
            txt_test_data.append({'server': match.group(1), 'port': match.group(2), 'link': link})

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_node_alive, txt_test_data))
        for item, is_alive in zip(txt_test_data, results):
            if is_alive: fast_txt_links.append(item['link'])

    # 4. 写入精选文件
    with open("fast_nodes.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"proxies": fast_proxies}, f, allow_unicode=True, sort_keys=False)
    with open("fast_nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(fast_txt_links))
        
    print(f"✨ 处理完成！全量: {len(seen_ips)} | 精选: {len(fast_proxies) + len(fast_txt_links)}")

if __name__ == "__main__":
    universal_mirror_factory()
