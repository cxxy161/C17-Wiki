import os
import subprocess
import re
from datetime import datetime
from openai import OpenAI

# 1. 初始化 NVIDIA 客户端
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

def get_git_diff():
    try:
        return subprocess.check_output(['git', 'diff', 'HEAD^', 'HEAD']).decode('utf-8')
    except Exception as e:
        print(f"获取 Diff 失败: {e}")
        return ""

def get_current_version():
    """从日志文件中提取当前最新的版本号"""
    file_path = 'src/content/docs/changelog.md'
    if not os.path.exists(file_path):
        return "0.1.0"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 匹配 #### v1.2.3 格式
        match = re.search(r'#### v(\d+\.\d+\.\d+)', content)
        return match.group(1) if match else "0.1.0"

def bump_version(current_v, level):
    """根据 AI 判断的级别计算新版本号"""
    major, minor, patch = map(int, current_v.split('.'))
    if level == "Major":
        major += 1
        minor = 0
        patch = 0
    elif level == "Minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"

def generate_summary_and_level(diff):
    """调用 AI 生成总结并判断更新等级"""
    if not diff or "src/content/docs/changelog.md" in diff and len(diff.splitlines()) < 10:
        return None, None

    try:
        # 在提示词中保留你原本的所有要求，并增加版本判断指令
        prompt = (
            "你是一个科幻设定集物理词条编辑。首先，请分析 Git 变更的量级，并输出更新等级：\n"
            "- Major: 核心设定重构、大规模架构调整或删除重大板块。\n"
            "- Minor: 新增星球、种族、舰船等完整词条，或增加显著新内容。\n"
            "- Patch: 修正错别字、微调数值、格式优化或小幅语句完善。\n\n"
            "你的回答必须严格遵循以下格式：\n"
            "LEVEL: [级别]\n"
            "SUMMARY: [你的总结内容]\n\n"
            "关于 SUMMARY 的要求：简练的更新日志（每个点20字以内，不含废话和表情包，正确使用md格式）。按更新内容分点列出。"
            "善于使用'修改了'、'增加了'、'完善了'等开头，直接描述设定点。\n\n"
            f"内容如下：\n{diff}"
        )

        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-v4-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        
        res = completion.choices[0].message.content.strip()
        
        # 解析 AI 的回复
        level_match = re.search(r'LEVEL:\s*(Major|Minor|Patch)', res, re.I)
        summary_match = re.search(r'SUMMARY:\s*(.*)', res, re.S)
        
        level = level_match.group(1).capitalize() if level_match else "Patch"
        summary = summary_match.group(1).strip() if summary_match else "完善了部分设定。"
        
        return level, summary
    except Exception as e:
        print(f"AI 生成失败: {e}")
        return None, None

def insert_log_to_file(level, summary):
    file_path = 'src/content/docs/changelog.md'
    if not os.path.exists(file_path):
        return

    current_v = get_current_version()
    new_v = bump_version(current_v, level)
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    # 包含版本号的新标题格式
    new_entry = (
        f"#### v{new_v} ({date_str})\n\n"
        f"{summary}\n\n"
        f"---\n\n"
    )

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    marker = "`LOG`"
    try:
        index = next(i for i, line in enumerate(lines) if marker in line)
        lines.insert(index + 1, new_entry)
    except StopIteration:
        lines.append(new_entry)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    diff_content = get_git_diff()
    level, summary_text = generate_summary_and_level(diff_content)
    
    if summary_text:
        insert_log_to_file(level, summary_text)
    else:
        print("无有效变更，跳过更新。")
