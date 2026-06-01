# -*- coding: utf-8 -*-
"""
Chatbot Baseline — No tools, no reasoning loop.
The LLM just guesses an answer directly without any game data access.
Used to compare against the ReAct Agent.
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from src.core.gemini_provider import GeminiProvider
from src.core.openai_provider import OpenAIProvider
from src.telemetry.logger import logger

load_dotenv()


def main():
    print("=" * 60)
    print("🤖 OPTC Pirate Rumble — CHATBOT BASELINE (No Tools)")
    print("=" * 60)

    # Initialize LLM
    provider = os.getenv("DEFAULT_PROVIDER", "google").lower()
    model = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    if provider == "google":
        llm = GeminiProvider(model_name=model)
    else:
        llm = OpenAIProvider(model_name=model)
    print(f"Provider: {provider} | Model: {model}\n")

    # Test queries
    queries = [
        "Tôi cần xây team đánh đội Five Elders gồm Imu (STR, Powerhouse/Driven), Saturn (STR, Driven/Cerebral) và Mars (STR, Driven/Shooter). Box tôi có: Shanks, Buggy, Blackbeard, Kuma, Luffy&Bonney, Luffy&Broggy, Luffy Emperor, Vegapunk, Atlas, Lilith. Hãy đề xuất team tối ưu và chiến thuật.",
    ]

    for i, query in enumerate(queries):
        print(f"📝 Query {i+1}: {query[:100]}...")
        print("-" * 40)

        logger.log_event("CHATBOT_QUERY", {"query": query})

        result = llm.generate(query)
        response = result["content"]

        logger.log_event("CHATBOT_RESPONSE", {
            "response": response[:300],
            "usage": result["usage"],
            "latency_ms": result["latency_ms"]
        })

        print(f"💬 Chatbot:\n{response}")
        print(f"\n⏱️ Latency: {result['latency_ms']}ms | Tokens: {result['usage']['total_tokens']}")
        print("=" * 60)


if __name__ == "__main__":
    main()
