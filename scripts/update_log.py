import os
import subprocess
from datetime import datetime
from openai import OpenAI

# 1. 初始化 NVIDIA 客户端
# 确保在 GitHub Secrets 中配置了 NVIDIA_API_KEY
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

def get_git_diff():
    """获取最后一次提交的差异内容"""
    try:
        # HEAD^ 指向上一个提交，HEAD 是当前提交
        return subprocess.check_output(['git', 'diff', 'HEAD^', 'HEAD']).decode('utf-8')
    except Exception as e:
        print(f"获取 Diff 失败: {e}")
        return ""

def generate_summary(diff):
    """调用 AI 生成极简总结"""
    # 过滤掉只有日志文件变动的情况，防止套娃
    if not diff or "src/content/docs/changelog.md" in diff and len(diff.splitlines()) < 10:
        return None

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-v4-flash",
            messages=[{
                "role": "user", 
                "content": f"你是一个科幻设定集物理词条编辑。请根据以下 Git 变更内容，总结出一条简练的更新日志（每个点20字以内，不含废话和表情包，正确使用md格式）。善于使用'修改了'、'增加了'等开头，直接描述设定点。\n\n内容如下：\n{diff}"
            }],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI 生成失败: {e}")
        return None

def insert_log_to_file(summary):
    """将日志精准插入到标识符 [LOG_MARKER] 下方"""
    file_path = 'src/content/docs/changelog.md'
    
    # 确保文件存在
    if not os.path.exists(file_path):
        print(f"找不到文件: {file_path}")
        return

    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    new_entry = f"* **{date_str}**: {summary}\n"

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 寻找标识符位置
    marker = "`LOG`"
    try:
        # 找到包含标识符的那一行索引
        index = next(i for i, line in enumerate(lines) if marker in line)
        # 在标识符下一行插入
        lines.insert(index + 1, new_entry)
        print(f"成功注入日志: {summary}")
    except StopIteration:
        # 如果没找到标识符，就追加到末尾
        lines.append(new_entry)
        print("未找到标识符，已追加到文件末尾")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    # 流程：抓取差异 -> AI 总结 -> 写入文件
    diff_content = get_git_diff()
    summary_text = generate_summary(diff_content)
    
    if summary_text:
        insert_log_to_file(summary_text)
    else:
        print("无有效变更或 AI 未生成总结，跳过更新。")
