# -*- coding: utf-8 -*-
"""
OPTC Pirate Rumble — Tool Registry
Registers all available tools with descriptions for the ReAct Agent.
"""

from src.tools.optc_tools import (
    analyze_enemy,
    get_type_matchup,
    search_box,
    check_leader_synergy,
    build_team_plan,
)

TOOLS = [
    {
        "name": "analyze_enemy",
        "description": (
            "Phân tích chi tiết team địch: thành viên, type, classes, khả năng, mối đe dọa, và điểm yếu. "
            "Input: team_id (string). Ví dụ: analyze_enemy(\"team_imu\")"
        ),
        "function": analyze_enemy,
    },
    {
        "name": "get_type_matchup",
        "description": (
            "Kiểm tra tương quan type (hệ tương khắc): mạnh hơn, yếu hơn, trung lập. "
            "Input: type_name (STR/DEX/QCK/PSY/INT). Ví dụ: get_type_matchup(\"STR\")"
        ),
        "function": get_type_matchup,
    },
    {
        "name": "search_box",
        "description": (
            "Tìm nhân vật trong box người chơi theo tiêu chí. "
            "Input: criteria (string). Các cách dùng:\n"
            "  - search_box(\"all\") — xem tất cả units\n"
            "  - search_box(\"type=QCK\") — lọc theo type\n"
            "  - search_box(\"class=Cerebral\") — lọc theo class\n"
            "  - search_box(\"counter=Ability Bind\") — tìm units counter debuff cụ thể\n"
            "  - search_box(\"has=Heal\") — tìm units có khả năng cụ thể\n"
            "  - search_box(\"faction=Four Emperors\") — lọc theo faction"
        ),
        "function": search_box,
    },
    {
        "name": "check_leader_synergy",
        "description": (
            "Kiểm tra leader skill có buff được các members không. ID đầu tiên là leader. "
            "Input: danh sách IDs cách nhau bởi dấu phẩy. "
            "Ví dụ: check_leader_synergy(\"4562, 4492, 4490, 4137, 4082\")"
        ),
        "function": check_leader_synergy,
    },
    {
        "name": "build_team_plan",
        "description": (
            "Đánh giá tổng thể team plan so với enemy: type coverage, debuff counter, leader synergy, special interactions. "
            "Input: 'id1, id2, ... vs enemy_team_id'. ID đầu tiên là leader. "
            "Ví dụ: build_team_plan(\"4562, 4492, 4490, 4137, 4082 vs team_imu\")"
        ),
        "function": build_team_plan,
    },
]
