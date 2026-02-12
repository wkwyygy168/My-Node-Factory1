import requests
import base64

def dual_mirror_factory():
    # 你的两个核心源
    yaml_source = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    b64_source = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    
    try:
        # --- 镜像 1：搬运 YAML ---
        print("正在镜像 YAML 源...")
        yaml_data = requests.get(yaml_source, timeout=15).text
        with open("nodes.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_data)
            
        # --- 镜像 2：搬运 Base64 (自动解密) ---
        print("正在镜像 Base64 源...")
        b64_raw = requests.get(b64_source, timeout=15).text.strip()
        # 补齐位并尝试解码
        b64_raw += "=" * (-len(b64_raw) % 4)
        try:
            decoded_data = base64.b64decode(b64_raw).decode('utf-8', errors='ignore')
            final_b64_content = decoded_data
        except:
            final_b64_content = b64_raw # 解不开就原样搬运
            
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(final_b64_content)
            
        print("✅ 双轨镜像全部完成！")
        
    except Exception as e:
        print(f"❌ 搬运失败: {e}")

if __name__ == "__main__":
    dual_mirror_factory()
