import os
import subprocess
import re
from datetime import datetime, timezone
from openai import OpenAI

# 1. 初始化 NVIDIA 客户端
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

def get_git_diff():
    """从水位线（上次日志更新点）开始比对，防止报错导致的记录丢失"""
    file_path = 'src/content/docs/changelog.md'
    try:
        last_log_commit = subprocess.check_output([
            'git', 'log', '-1', '--format=%H', '--', file_path
        ]).decode('utf-8').strip()

        if last_log_commit:
            diff_output = subprocess.check_output([
                'git', 'diff', last_log_commit, 'HEAD', '--', '*.md', '*.mdx'
            ]).decode('utf-8')
            
            if diff_output.strip():
                return diff_output
    except Exception as e:
        print(f"水位线查找失败（可能是首次运行）: {e}")
    
    # 兜底逻辑
    try:
        return subprocess.check_output([
            'git', 'diff', 'HEAD^', 'HEAD', '--', '*.md', '*.mdx'
        ]).decode('utf-8')
    except:
        return ""

def get_current_version():
    """从日志文件中提取当前最新的版本号"""
    file_path = 'src/content/docs/changelog.md'
    if not os.path.exists(file_path):
        return "0.1.0"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
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
        prompt = (
            "你是一个逻辑严密的科幻设定集编辑。请分析 Git Diff，按以下逻辑生成版本日志：\n\n"
            "【逻辑模版（灵活运用）】\n"
            "1. 新增：新增了[词条名]词条，主要涉及[核心设定简述]。\n"
            "2. 完善：完善了[词条名]词条，补充了[具体增加的内容]。\n"
            "3. 修正：修改了[词条名]词条，修正了[错别字/数据错误/描述优化]（无需展开细节）。\n"
            "4. 其他：根据实际情况使用‘合并’、‘删除’、‘移动’、‘整理’等动词，描述清晰、不啰嗦。\n\n"
            "【核心要求】\n"
            "- 合并同类项：如果是一个文件的变动，只能输出一个条目，不要拆分。建议每个文件对应一个列表点（*）。\n"
            "- 字数控制：每个条目控制在 20-30 字以内。\n"
            "- 判定标准：\n"
            "  - Major: 核心设定重构、删除重大板块。\n"
            "  - Minor: 新增完整的星球、种族、技术词条。\n"
            "  - Patch: 修正、润色、格式优化。\n\n"
            "【输出格式（严格执行）】\n"
            "LEVEL: [级别]\n"
            "SUMMARY: [你的总结内容]\n\n"
            f"待分析内容：\n{diff[:5000]}"
        )

        # 彻底移除 timeout 限制，让它死等
        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-v4-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        
        res = completion.choices[0].message.content.strip()
        
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
    
    # 获取 UTC 时间并生成埋点标签
    now_utc = datetime.now(timezone.utc)
    date_iso = now_utc.isoformat()
    display_utc = now_utc.strftime('%Y-%m-%d %H:%M')

    # 如果 AI 没写列表符，自动补上
    formatted_summary = summary if summary.startswith(("*", "1.")) else f"* {summary}"

    new_entry = (
        f"#### v{new_v} (<span class='log-date' data-time='{date_iso}'>{display_utc} UTC</span>)\n\n"
        f"{formatted_summary}\n\n"
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
