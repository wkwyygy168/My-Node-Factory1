import requests
import base64
import re

def move_house():
    # 两个源
    yaml_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    b64_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    
    try:
        # 1. 先拿 all.yaml 作为基础（保持它的格式不变）
        yaml_content = requests.get(yaml_url, timeout=15).text
        
        # 2. 拿 base64.txt 并解密出里面的节点链接
        b64_raw = requests.get(b64_url, timeout=15).text.strip()
        missing_padding = len(b64_raw) % 4
        if missing_padding:
            b64_raw += "=" * (4 - missing_padding)
        decoded_nodes = base64.b64decode(b64_raw).decode('utf-8', errors='ignore')
        
        # 提取出 base64 里的纯链接
        extra_nodes = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', decoded_nodes, re.I)
        
        # 3. 将额外节点拼成字符串，准备塞进 YAML
        # 注意：YAML 格式中，节点通常是在 'proxies:' 下方的
        extra_nodes_str = "\n".join(extra_nodes)
        
        # 4. 暴力合并：把 base64 的节点直接接在 YAML 内容后面
        # 为了不破坏 YAML 结构，我们在中间加个换行
        final_output = yaml_content + "\n# Extra Nodes from Base64\n" + extra_nodes_str
            
        # 5. 存入你的仓库
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(final_output)
            
        print("✅ 以 YAML 为主的镜像搬运完成！")
        
    except Exception as e:
        print(f"❌ 搬运失败: {e}")

if __name__ == "__main__":
    move_house()
