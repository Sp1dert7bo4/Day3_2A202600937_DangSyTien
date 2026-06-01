# -*- coding: utf-8 -*-
"""
ReAct Agent Runner — OPTC Pirate Rumble Strategy Agent
Runs the full Thought-Action-Observation loop with 5 tools.
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from src.core.gemini_provider import GeminiProvider
from src.core.openai_provider import OpenAIProvider
from src.agent.agent import ReActAgent
from src.tools.tool_registry import TOOLS
from src.telemetry.logger import logger

load_dotenv()


def main():
    print("=" * 60)
    print("🏴‍☠️ OPTC Pirate Rumble — ReAct STRATEGY AGENT")
    print("=" * 60)

    # Initialize LLM
    provider = os.getenv("DEFAULT_PROVIDER", "google").lower()
    model = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    if provider == "google":
        llm = GeminiProvider(model_name=model)
    else:
        llm = OpenAIProvider(model_name=model)
    print(f"Provider: {provider} | Model: {model}")
    print(f"Tools: {', '.join(t['name'] for t in TOOLS)}")
    print(f"Max Steps: 8\n")

    # Initialize Agent
    agent = ReActAgent(llm=llm, tools=TOOLS, max_steps=8)

    # Choose between quick test or interactive chat mode
    print("=" * 60)
    try:
        # Prompt for chat mode
        mode = input("💬 Bạn có muốn chuyển sang chế độ TRÒ CHUYỆN TƯƠNG TÁC (Chat Mode) không? (y/n): ").strip().lower()
    except Exception:
        mode = "n"
    print("=" * 60)

    if mode == 'y':
        print("\n💬 CHẾ ĐỘ TRÒ CHUYỆN TƯƠNG TÁC VỚI REACT AGENT")
        print("Bạn có thể đặt câu hỏi chiến thuật hoặc yêu cầu lọc tướng.")
        print("Gõ 'exit' hoặc 'quit' để thoát.\n")
        
        while True:
            try:
                query = input("\n👤 Bạn: ").strip()
                if not query:
                    continue
                if query.lower() in ['exit', 'quit']:
                    print("Tạm biệt!")
                    break
                
                print("\n🧠 Agent đang suy nghĩ...")
                answer = agent.run(query)
                
                print("\n🤖 Agent:")
                print(answer)
                print("-" * 60)
            except KeyboardInterrupt:
                print("\nTạm biệt!")
                break
    else:
        # Quick test mode
        query = "Tôi cần xây team đánh đội Five Elders (team_imu) gồm Imu, Saturn và Mars. Hãy phân tích team địch, tìm counter phù hợp trong box của tôi, và đề xuất team tối ưu."
        print(f"📝 Query: {query}")
        print("=" * 60)
        print("🧠 Agent is thinking...\n")

        # Run agent
        answer = agent.run(query)

        print("=" * 60)
        print("✅ FINAL ANSWER:")
        print("=" * 60)
        print(answer)
        print("=" * 60)

        # Print summary
        if agent.history:
            last = agent.history[-1]
            print(f"\n📊 Agent completed in {last['steps']} steps")

    print(f"\n📁 Logs saved to: logs/")


if __name__ == "__main__":
    main()
