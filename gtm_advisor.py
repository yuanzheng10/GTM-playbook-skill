#!/usr/bin/env python3
"""
GTM 操盘手册 · AI 顾问 CLI
支持 Claude API 和 Gemini API，基于 GTM_playbook 知识库回答执行问题。

用法:
  python gtm_advisor.py "你的问题"
  python gtm_advisor.py --provider gemini "你的问题"
  python gtm_advisor.py --interactive
"""

import os
import sys
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── 读取 Skill 知识库 ─────────────────────────────────────────────────────────

SKILL_PATH = Path(__file__).parent.parent / "skill" / "SKILL.md"

def load_skill_content() -> str:
    """加载 SKILL.md 作为系统提示的知识库"""
    if not SKILL_PATH.exists():
        print(f"⚠️  找不到 SKILL.md，路径: {SKILL_PATH}", file=sys.stderr)
        return ""
    return SKILL_PATH.read_text(encoding="utf-8")

SYSTEM_PROMPT = """你是一位资深GTM（Go-To-Market）操盘顾问，专注于2C消费电子领域的产品上市、经营管理和跨境电商业务。

你的知识体系基于以下GTM操盘手册：

{skill_content}

---

回答原则：
1. 优先基于上述手册中的框架、表格和SOP来回答
2. 给出具体可操作的建议，而不是泛泛而谈
3. 涉及数据计算时，主动帮用户列出公式和算例
4. 如果问题超出手册范围，诚实说明，并给出通用最佳实践
5. 回答使用中文，专业术语保留英文缩写（如PSI、DOS、SKU等）
6. 结构化输出，善用表格和列表提升可读性
"""

# ── Claude API ────────────────────────────────────────────────────────────────

def ask_claude(question: str, history: list, skill_content: str) -> str:
    try:
        import anthropic
    except ImportError:
        return "❌ 请先安装: pip install anthropic"

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "❌ 未找到 ANTHROPIC_API_KEY，请在 .env 文件中设置"

    client = anthropic.Anthropic(api_key=api_key)

    messages = history + [{"role": "user", "content": question}]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT.format(skill_content=skill_content),
        messages=messages,
    )

    return response.content[0].text


# ── Gemini API ────────────────────────────────────────────────────────────────

def ask_gemini(question: str, history: list, skill_content: str) -> str:
    try:
        import google.generativeai as genai
    except ImportError:
        return "❌ 请先安装: pip install google-generativeai"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "❌ 未找到 GEMINI_API_KEY，请在 .env 文件中设置"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT.format(skill_content=skill_content),
    )

    # 将历史转换为 Gemini 格式
    gemini_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(question)
    return response.text


# ── 路由 ──────────────────────────────────────────────────────────────────────

PROVIDERS = {
    "claude": ask_claude,
    "gemini": ask_gemini,
}

def ask(question: str, provider: str, history: list, skill_content: str) -> str:
    fn = PROVIDERS.get(provider)
    if not fn:
        return f"❌ 不支持的 provider: {provider}，可选: {list(PROVIDERS.keys())}"
    return fn(question, history, skill_content)


# ── 交互模式 ──────────────────────────────────────────────────────────────────

def interactive_mode(provider: str, skill_content: str):
    print(f"\n🟢 GTM 操盘顾问 · 交互模式（{provider}）")
    print("   输入问题后回车，输入 'quit' 或 Ctrl+C 退出\n")
    print("─" * 60)

    history = []

    while True:
        try:
            user_input = input("\n你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q", "退出"):
            print("👋 再见！")
            break

        print("\n💬 GTM顾问: ", end="", flush=True)
        answer = ask(user_input, provider, history, skill_content)
        print(answer)

        # 保存对话历史（保留最近10轮）
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})
        if len(history) > 20:
            history = history[-20:]


# ── 主入口 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="GTM 操盘手册 AI 顾问",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python gtm_advisor.py "新品上市前8周GTM要做什么？"
  python gtm_advisor.py --provider gemini "如何计算产品销售毛利率？"
  python gtm_advisor.py --interactive
  python gtm_advisor.py --interactive --provider gemini
        """
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="要提问的问题（不填则进入交互模式）"
    )
    parser.add_argument(
        "--provider", "-p",
        choices=list(PROVIDERS.keys()),
        default="claude",
        help="AI 提供商（默认: claude）"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="进入交互对话模式"
    )
    parser.add_argument(
        "--skill-path",
        type=str,
        help="自定义 SKILL.md 路径（可选）"
    )

    args = parser.parse_args()

    # 加载知识库
    global SKILL_PATH
    if args.skill_path:
        SKILL_PATH = Path(args.skill_path)
    skill_content = load_skill_content()

    if not skill_content:
        print("⚠️  知识库为空，将使用内置 GTM 通用知识回答", file=sys.stderr)

    # 执行
    if args.interactive or not args.question:
        interactive_mode(args.provider, skill_content)
    else:
        answer = ask(args.question, args.provider, [], skill_content)
        print(answer)


if __name__ == "__main__":
    main()
