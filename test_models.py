import os
from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider
from src.agent.agent import ReActAgent
from src.tools.tool_registry import TOOLS

load_dotenv()

print("Initializing OpenAIProvider for DeepSeek...")
llm = OpenAIProvider(model_name=os.getenv("DEFAULT_MODEL"))
agent = ReActAgent(llm=llm, tools=TOOLS)

# Simulate history at step 1
user_input = "Tôi cần xây team đánh đội Five Elders (team_imu) gồm Imu, Saturn và Mars. Hãy phân tích team địch, tìm counter phù hợp trong box của tôi, và đề xuất team tối ưu."
llm_response = 'Thought: Đầu tiên tôi cần phân tích team địch "team_imu" để hiểu thành phần, type, class, khả năng, mối đe dọa và điểm yếu trước khi tìm cách khắc chế.\n\nAction: analyze_enemy("team_imu")'

# Let's get the real tool output
print("Executing tool analyze_enemy...")
from src.tools.optc_tools import analyze_enemy
observation = analyze_enemy("team_imu")

# Construct conversation history as it would be at step 1
conversation = f"{user_input}\n{llm_response}\nObservation: {observation}"

print(f"Conversation length: {len(conversation)} characters")
print("Calling LLM generate for step 1...")
try:
    result = llm.generate(conversation, system_prompt=agent.get_system_prompt())
    print("✅ Success!")
    print(f"Content: {result['content'][:500]}")
except Exception as e:
    print(f"❌ Failed: {e}")
