import requests
import base64

def move_house():
    # 1. 目标源：这里现在放了两个镜像源
    target_urls = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    ]
    
    combined_content = ""
    
    # 2. 这里的循环是必须加的，否则它不知道怎么处理两条链接
    for url in target_urls:
        try:
            response = requests.get(url, timeout=15)
            raw_content = response.text.strip()
            
            # 3. 搬运逻辑（完全保留你原来的解密尝试）
            try:
                temp_content = raw_content
                missing_padding = len(temp_content) % 4
                if missing_padding:
                    temp_content += "=" * (4 - missing_padding)
                decoded_data = base64.b64decode(temp_content).decode('utf-8', errors='ignore')
                combined_content += decoded_data + "\n"
            except:
                # 如果解不开（比如 all.yaml），就直接原样搬运
                combined_content += raw_content + "\n"
                
        except Exception as e:
            print(f"❌ 搬运源 {url} 失败: {e}")

    # 4. 存入你的仓库文件
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
            
    print("✅ 订阅源镜像搬运成功！两条链接的内容都已同步。")

if __name__ == "__main__":
    move_house()
