import requests
import base64

def dual_mirror_factory():
    # 1. 把你所有的源都扔在这里，脚本会自动按后缀分家
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt"
    ]
    
    yaml_combined = ""
    txt_combined = ""
    
    try:
        for url in sources:
            print(f"正在处理: {url}")
            response = requests.get(url, timeout=15)
            content = response.text.strip()
            
            # --- 逻辑 A：如果是 .yaml 源 ---
            if url.endswith(".yaml"):
                # 镜像搬运，多个 YAML 之间加个分隔符防止连在一起
                yaml_combined += content + "\n---\n"
                
            # --- 逻辑 B：如果是 .txt 源 ---
            else:
                # 尝试补齐 Base64 位并解密
                temp_raw = content + "=" * (-len(content) % 4)
                try:
                    decoded = base64.b64decode(temp_raw).decode('utf-8', errors='ignore')
                    # 如果解出来确实像节点链接，就用解开后的
                    if "://" in decoded:
                        txt_combined += decoded + "\n"
                    else:
                        txt_combined += content + "\n"
                except:
                    # 解不开就原样镜像搬运
                    txt_combined += content + "\n"
        
        # --- 最终写入各自的文件 ---
        with open("nodes.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_combined)
            
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(txt_combined)
            
        print("✅ 订阅源分类镜像全部完成！")
        
    except Exception as e:
        print(f"❌ 运行过程中出错: {e}")

if __name__ == "__main__":
    dual_mirror_factory()
