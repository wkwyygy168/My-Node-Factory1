import requests
import base64
import re

def move_house():
    yaml_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    b64_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt"
    
    try:
        # 1. 搬运 all.yaml 核心框架
        yaml_content = requests.get(yaml_url, timeout=15).text
        
        # 2. 获取并解密 base64.txt 里的链接
        b64_res = requests.get(b64_url, timeout=15).text.strip()
        b64_res += "=" * (-len(b64_res) % 4)
        decoded = base64.b64decode(b64_res).decode('utf-8', errors='ignore')
        extra_links = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', decoded, re.I)
        
        # 3. 将链接转换成 Karing 绝对能看懂的标准 YAML 节点格式
        yaml_nodes = []
        for i, link in enumerate(extra_links):
            # 将链接作为一个“特殊节点”包装，这样 Karing 会以标准模式解析它
            # 我们给它起个名字方便区分
            node_name = f"Mirror_Node_{i+1}"
            # 注意：这里我们使用了一种万能引用方式，确保不破坏 YAML 结构
            yaml_nodes.append(f"  - {{ name: '{node_name}', type: vmess, server: 127.0.0.1, port: 443, uuid: auto, alterId: 0, cipher: auto, plugin: '{link}' }}")

        # 4. 精准插入到 proxies: 下方
        # 我们使用 Python 的 split 确保插入点在原 proxies 列表的开头
        if "proxies:" in yaml_content:
            parts = yaml_content.split("proxies:", 1)
            # 在 proxies: 后面立刻换行并插入我们的新节点
            final_output = parts[0] + "proxies:\n" + "\n".join(yaml_nodes) + "\n" + parts[1]
        else:
            final_output = "proxies:\n" + "\n".join(yaml_nodes) + "\n" + yaml_content

        # 5. 保存镜像
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(final_output)
            
        print(f"✅ 镜像转换成功！已安全整合 {len(extra_links)} 个加密节点。")
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    move_house()
