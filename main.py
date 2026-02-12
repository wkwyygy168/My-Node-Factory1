import requests
import base64

def dual_mirror_factory():
    # 1. 分类你的 4 条镜像源
    yaml_sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.yaml"
    ]
    
    txt_sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt"
    ]
    
    # --- 处理 YAML 镜像 ---
    combined_yaml = ""
    for url in yaml_sources:
        try:
            print(f"正在镜像 YAML: {url}")
            content = requests.get(url, timeout=15).text
            combined_yaml += content + "\n---\n" # 用 YAML 分隔符连接
        except Exception as e:
            print(f"YAML 镜像失败 {url}: {e}")

    with open("nodes.yaml", "w", encoding="utf-8") as f:
        f.write(combined_yaml)

    # --- 处理 TXT/Base64 镜像 ---
    combined_txt = ""
    for url in txt_sources:
        try:
            print(f"正在镜像 TXT: {url}")
            raw = requests.get(url, timeout=15).text.strip()
            # 尝试解密 Base64
            try:
                temp_raw = raw + "=" * (-len(raw) % 4)
                decoded = base64.b64decode(temp_raw).decode('utf-8', errors='ignore')
                if "://" in decoded:
                    combined_txt += decoded + "\n"
                else:
                    combined_txt += raw + "\n"
            except:
                combined_txt += raw + "\n"
        except Exception as e:
            print(f"TXT 镜像失败 {url}: {e}")

    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(combined_txt)
        
    print("✅ 4条源全量镜像完成！已生成 nodes.yaml 和 nodes.txt")

if __name__ == "__main__":
    dual_mirror_factory()
