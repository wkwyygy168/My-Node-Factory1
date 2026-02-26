import requests
import base64
import yaml
import re

def universal_mirror_factory():
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt"
    ]
    
    final_proxies = []
    txt_links = []
    seen_ips = set()

    for url in sources:
        try:
            print(f"🚀 正在处理: {url}")
            res = requests.get(url, timeout=15)
            content = res.text
            
            # --- 逻辑 A: 结构化解析 YAML ---
            if ".yaml" in url or "clash" in url.lower():
                try:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict) and 'proxies' in data:
                        for p in data['proxies']:
                            # 指纹去重: server + port
                            fp = f"{p.get('server')}:{p.get('port')}"
                            if fp not in seen_ips:
                                seen_ips.add(fp)
                                final_proxies.append(p)
                except: pass

            # --- 逻辑 B: 解析 TXT/Base64 ---
            try:
                # 自动补齐 Base64 填充
                decoded = content
                if "://" not in content[:50]:
                    try:
                        decoded = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
                    except: pass
                
                for line in decoded.splitlines():
                    if "://" in line:
                        # 链接去重
                        core = line.split('#')[0]
                        if core not in seen_ips:
                            seen_ips.add(core)
                            txt_links.append(line)
            except: pass

        except Exception as e:
            print(f"❌ 失败 {url}: {e}")

    # --- 写入文件 ---
    # 写入 nodes.yaml (由 yaml 库生成，绝不会出现重复 key)
    with open("nodes.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"proxies": final_proxies}, f, allow_unicode=True, sort_keys=False)
    
    # 写入 nodes.txt
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(txt_links))
        
    print(f"✨ 处理完成！当前有效唯一节点数: {len(seen_ips)}")

if __name__ == "__main__":
    universal_mirror_factory()
