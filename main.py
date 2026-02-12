import requests
import base64

def move_house():
    # 1. 目标源（你想搬运的 Gist 订阅链接）
    target_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    
    try:
        # 2. 下载内容
        response = requests.get(target_url, timeout=15)
        raw_content = response.text.strip()
        
        # 3. 搬运逻辑：
        # 如果它是 Base64 加密的，咱们把它解开，变成明文存进 nodes.txt
        # 这样你在 Karing 里看的时候更清晰
        try:
            # 自动补齐 Base64 填充符
            missing_padding = len(raw_content) % 4
            if missing_padding:
                raw_content += "=" * (4 - missing_padding)
            decoded_content = base64.b64decode(raw_content).decode('utf-8', errors='ignore')
            final_data = decoded_content
        except:
            # 如果不是加密的，就直接原样搬运
            final_data = raw_content
            
        # 4. 存入你的仓库文件
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(final_data)
            
        print("✅ 搬运成功！内容已同步到你的仓库。")
        
    except Exception as e:
        print(f"❌ 搬运失败: {e}")

if __name__ == "__main__":
    move_house()
