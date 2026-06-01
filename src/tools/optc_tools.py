# -*- coding: utf-8 -*-
"""
OPTC Pirate Rumble — Strategy Tools
5 tools for the ReAct Agent to analyze enemies, search counters, and build teams.
"""

from src.tools.optc_data import CHARACTERS, ENEMY_TEAMS, PLAYER_BOX, TYPE_ADVANTAGE


def analyze_enemy(team_id: str) -> str:
    """Phân tích chi tiết team địch: thành viên, khả năng, mối đe dọa, điểm yếu."""
    team_id = team_id.strip().strip('"').strip("'")
    
    if team_id not in ENEMY_TEAMS:
        available = ", ".join(ENEMY_TEAMS.keys())
        return f"Team '{team_id}' không tồn tại. Các team có sẵn: {available}"
    
    team = ENEMY_TEAMS[team_id]
    all_ids = [team["leader_id"]] + team["member_ids"]
    
    lines = [f"{'='*60}", f"ENEMY TEAM: {team['name']}", f"{'='*60}", ""]
    
    # List each member
    all_types = []
    all_classes = set()
    all_threats = []
    all_inflicts = set()
    
    for i, cid in enumerate(all_ids):
        char = CHARACTERS[cid]
        role = "LEADER" if i == 0 else f"MEMBER {i}"
        all_types.append(char["type"])
        all_classes.update(char["classes"])
        all_threats.extend(char["tags"].get("threats", []))
        all_inflicts.update(char["tags"].get("inflicts", []))
        
        lines.append(f"[{role}] #{char['id']} {char['name']}")
        lines.append(f"  Type: {char['type']} | Classes: {', '.join(char['classes'])} | CT: {char['ct']}")
        lines.append(f"  Special: {char['special'][:150]}...")
        lines.append(f"  GP Burst: {char['gp_burst'][:120]}...")
        lines.append(f"  Key Threats: {', '.join(char['tags'].get('threats', ['None']))}")
        lines.append("")
    
    # Threat analysis
    lines.append(f"{'='*60}")
    lines.append("THREAT ANALYSIS")
    lines.append(f"{'='*60}")
    
    lines.append(f"\n🔴 DEBUFFS ENEMY INFLICTS: {', '.join(all_inflicts) if all_inflicts else 'None'}")
    
    lines.append(f"\n🔴 KEY THREATS:")
    for t in all_threats:
        lines.append(f"  - {t}")
    
    lines.append(f"\n🟡 TEAM COMPOSITION:")
    lines.append(f"  - Types: {', '.join(all_types)} (ALL {all_types[0]})" if len(set(all_types)) == 1 else f"  - Types: {', '.join(all_types)}")
    lines.append(f"  - Classes: {', '.join(all_classes)}")
    
    # Weaknesses
    if len(set(all_types)) == 1:
        weak_type = TYPE_ADVANTAGE[all_types[0]]["weak_against"]
        lines.append(f"\n🟢 POTENTIAL WEAKNESSES:")
        lines.append(f"  - ALL members are {all_types[0]} → VULNERABLE to {weak_type} type")
    
    # Leader skill analysis
    leader = CHARACTERS[team["leader_id"]]
    lines.append(f"\n🟡 LEADER SKILL ({leader['name']}):")
    lines.append(f"  {leader['leader_skill']}")
    
    return "\n".join(lines)


def get_type_matchup(type_name: str) -> str:
    """Kiểm tra tương quan type: mạnh/yếu/trung lập."""
    type_name = type_name.strip().strip('"').strip("'").upper()
    
    if type_name not in TYPE_ADVANTAGE:
        return f"Type '{type_name}' không hợp lệ. Các type: STR, DEX, QCK, PSY, INT"
    
    info = TYPE_ADVANTAGE[type_name]
    lines = [
        f"=== TYPE MATCHUP: {type_name} ===",
        f"✅ {type_name} STRONG against {info['strong_against']} (deals 2x damage)",
        f"❌ {type_name} WEAK against {info['weak_against']} (deals 0.5x damage)",
        f"➖ Neutral with: {', '.join(info['neutral'])}",
        "",
        "=== FULL TYPE TRIANGLE ===",
        "STR → DEX → QCK → STR (triangle)",
        "PSY ↔ INT (mutual advantage/disadvantage)",
    ]
    return "\n".join(lines)


def search_box(criteria: str) -> str:
    """Tìm nhân vật trong box theo tiêu chí: type, class, counter, hoặc all."""
    criteria = criteria.strip().strip('"').strip("'").lower()
    
    results = []
    
    if criteria == "all":
        # Show all units in box
        for cid in PLAYER_BOX:
            char = CHARACTERS[cid]
            results.append(char)
    
    elif criteria.startswith("type="):
        filter_type = criteria.split("=")[1].strip().upper()
        for cid in PLAYER_BOX:
            char = CHARACTERS[cid]
            if char["type"] == filter_type:
                results.append(char)
    
    elif criteria.startswith("class="):
        filter_class = criteria.split("=")[1].strip().title()
        for cid in PLAYER_BOX:
            char = CHARACTERS[cid]
            if any(filter_class.lower() in c.lower() for c in char["classes"]):
                results.append(char)
    
    elif criteria.startswith("counter="):
        counter_target = criteria.split("=")[1].strip()
        for cid in PLAYER_BOX:
            char = CHARACTERS[cid]
            counters = char["tags"].get("counters", [])
            provides = char["tags"].get("provides", [])
            all_abilities = " ".join([
                str(counters), str(provides),
                char.get("special", ""), char.get("gp_burst", ""), char.get("ability", "")
            ]).lower()
            if counter_target.lower() in all_abilities:
                results.append(char)
    
    elif criteria.startswith("has="):
        search_term = criteria.split("=")[1].strip()
        for cid in PLAYER_BOX:
            char = CHARACTERS[cid]
            provides = char["tags"].get("provides", [])
            all_text = " ".join([
                str(provides), char.get("special", ""),
                char.get("gp_burst", ""), char.get("ability", "")
            ]).lower()
            if search_term.lower() in all_text:
                results.append(char)
    
    elif criteria.startswith("faction="):
        filter_faction = criteria.split("=")[1].strip()
        for cid in PLAYER_BOX:
            char = CHARACTERS[cid]
            if any(filter_faction.lower() in f.lower() for f in char.get("factions", [])):
                results.append(char)
    
    else:
        return (
            f"Criteria '{criteria}' không hợp lệ.\n"
            "Cách dùng:\n"
            "  search_box(\"all\") — xem tất cả units trong box\n"
            "  search_box(\"type=QCK\") — lọc theo type\n"
            "  search_box(\"class=Cerebral\") — lọc theo class\n"
            "  search_box(\"counter=Ability Bind\") — tìm units counter debuff\n"
            "  search_box(\"has=Heal\") — tìm units có khả năng cụ thể\n"
            "  search_box(\"faction=Four Emperors\") — lọc theo faction"
        )
    
    if not results:
        return f"Không tìm thấy unit nào trong box với tiêu chí: '{criteria}'"
    
    lines = [f"=== SEARCH RESULTS ({len(results)} units found for '{criteria}') ===", ""]
    for char in results:
        lines.append(f"#{char['id']} {char['name']}")
        lines.append(f"  Type: {char['type']} | Classes: {', '.join(char['classes'])} | CT: {char['ct']}")
        lines.append(f"  Factions: {', '.join(char['factions']) if char['factions'] else 'None'}")
        lines.append(f"  Provides: {', '.join(char['tags'].get('provides', []))}")
        lines.append(f"  Counters: {', '.join(char['tags'].get('counters', [])) if char['tags'].get('counters') else 'None'}")
        lines.append(f"  Inflicts: {', '.join(char['tags'].get('inflicts', [])) if char['tags'].get('inflicts') else 'None'}")
        lines.append("")
    
    return "\n".join(lines)


def check_leader_synergy(team_str: str) -> str:
    """Kiểm tra synergy giữa leader skill và các members. Input: 'leader_id, member1_id, member2_id, ...'"""
    team_str = team_str.strip().strip('"').strip("'")
    
    try:
        ids = [int(x.strip()) for x in team_str.split(",")]
    except ValueError:
        return "Lỗi: Input phải là các ID cách nhau bởi dấu phẩy. Ví dụ: check_leader_synergy(\"4562, 4492, 4490\")"
    
    if len(ids) < 2:
        return "Cần ít nhất 2 IDs (1 leader + 1 member)"
    
    leader_id = ids[0]
    member_ids = ids[1:]
    
    if leader_id not in CHARACTERS:
        return f"Leader #{leader_id} không tồn tại trong database."
    
    leader = CHARACTERS[leader_id]
    filters = leader.get("leader_buff_filters", {})
    
    if not filters:
        return f"#{leader_id} {leader['name']} không có leader skill phù hợp (không có buff filters)."
    
    lines = [
        f"=== LEADER SYNERGY CHECK ===",
        f"LEADER: #{leader['id']} {leader['name']} ({leader['type']}, {'/'.join(leader['classes'])})",
        f"Leader Skill: {leader['leader_skill']}",
        "",
        "--- MEMBER COMPATIBILITY ---",
    ]
    
    buff_types = set(filters.get("types", []))
    buff_classes = set(filters.get("classes", []))
    buff_factions = set(filters.get("factions", []))
    
    total_members = len(member_ids)
    buffed_count = 0
    
    for mid in member_ids:
        if mid not in CHARACTERS:
            lines.append(f"  ❓ #{mid} — NOT FOUND in database")
            continue
        
        member = CHARACTERS[mid]
        matches = []
        mismatches = []
        
        # Check type match
        if member["type"] in buff_types:
            matches.append(f"Type {member['type']} ✅")
        elif buff_types:
            mismatches.append(f"Type {member['type']} (needs {', '.join(buff_types)})")
        
        # Check class match
        class_match = set(member["classes"]) & buff_classes
        if class_match:
            matches.append(f"Class {', '.join(class_match)} ✅")
        elif buff_classes:
            mismatches.append(f"Class {', '.join(member['classes'])} (needs {', '.join(buff_classes)})")
        
        # Check faction match
        faction_match = set(member.get("factions", [])) & buff_factions
        if faction_match:
            matches.append(f"Faction {', '.join(faction_match)} ✅")
        elif buff_factions:
            member_factions = member.get("factions", [])
            if member_factions:
                mismatches.append(f"Faction {', '.join(member_factions)} (needs {', '.join(buff_factions)})")
        
        is_buffed = len(matches) > 0
        if is_buffed:
            buffed_count += 1
        
        status = "✅ BUFFED" if is_buffed else "❌ NO BUFF"
        lines.append(f"\n  #{mid} {member['name']} ({member['type']}, {'/'.join(member['classes'])}) — {status}")
        if matches:
            lines.append(f"    Matches: {', '.join(matches)}")
        if mismatches:
            lines.append(f"    Mismatches: {', '.join(mismatches)}")
    
    # Summary
    synergy_pct = int((buffed_count / total_members) * 100) if total_members > 0 else 0
    lines.append(f"\n{'='*40}")
    lines.append(f"SYNERGY SCORE: {buffed_count}/{total_members} members buffed ({synergy_pct}%)")
    
    if synergy_pct >= 80:
        lines.append("📊 Excellent synergy!")
    elif synergy_pct >= 60:
        lines.append("📊 Good synergy, but some members miss buffs.")
    else:
        lines.append("📊 Poor synergy! Consider changing leader or members.")
    
    return "\n".join(lines)


def build_team_plan(plan_str: str) -> str:
    """Đánh giá tổng thể team plan. Input: 'id1, id2, ... vs team_id'"""
    plan_str = plan_str.strip().strip('"').strip("'")
    
    if " vs " not in plan_str.lower():
        return "Lỗi: Format phải là 'id1, id2, ... vs enemy_team_id'. Ví dụ: build_team_plan(\"4562, 4492, 4490, 4137, 4082 vs team_imu\")"
    
    parts = plan_str.lower().split(" vs ")
    try:
        team_ids = [int(x.strip()) for x in parts[0].split(",")]
    except ValueError:
        return "Lỗi: IDs phải là số. Ví dụ: build_team_plan(\"4562, 4492, 4490, 4137, 4082 vs team_imu\")"
    
    enemy_team_id = parts[1].strip()
    
    if enemy_team_id not in ENEMY_TEAMS:
        return f"Enemy team '{enemy_team_id}' không tồn tại."
    
    enemy_team = ENEMY_TEAMS[enemy_team_id]
    enemy_ids = [enemy_team["leader_id"]] + enemy_team["member_ids"]
    
    # Gather data
    my_chars = [CHARACTERS[cid] for cid in team_ids if cid in CHARACTERS]
    enemy_chars = [CHARACTERS[cid] for cid in enemy_ids if cid in CHARACTERS]
    
    if len(my_chars) < 2:
        return "Cần ít nhất 2 units trong team."
    
    lines = [f"{'='*60}", "TEAM PLAN EVALUATION", f"{'='*60}", ""]
    
    # 1. Type Coverage
    lines.append("📊 1. TYPE COVERAGE vs ENEMY:")
    enemy_types = [c["type"] for c in enemy_chars]
    my_types = [c["type"] for c in my_chars]
    
    type_score = 0
    for mc in my_chars:
        for ec in enemy_chars:
            if TYPE_ADVANTAGE.get(mc["type"], {}).get("strong_against") == ec["type"]:
                type_score += 1
                lines.append(f"  ✅ #{mc['id']} ({mc['type']}) has advantage over enemy {ec['type']}")
            elif TYPE_ADVANTAGE.get(mc["type"], {}).get("weak_against") == ec["type"]:
                type_score -= 1
                lines.append(f"  ❌ #{mc['id']} ({mc['type']}) has DISADVANTAGE vs enemy {ec['type']}")
    
    lines.append(f"  Type Score: {type_score}")
    lines.append("")
    
    # 2. Debuff Counter Coverage
    lines.append("📊 2. DEBUFF COUNTER COVERAGE:")
    enemy_debuffs = set()
    for ec in enemy_chars:
        enemy_debuffs.update(ec["tags"].get("inflicts", []))
    
    my_counters = set()
    for mc in my_chars:
        my_counters.update(mc["tags"].get("counters", []))
        for p in mc["tags"].get("provides", []):
            if any(keyword in p.lower() for keyword in ["cleanse", "evade", "reduce", "immunity"]):
                my_counters.add(p)
    
    covered = enemy_debuffs & my_counters if my_counters else set()
    uncovered = enemy_debuffs - my_counters if my_counters else enemy_debuffs
    
    for d in covered:
        lines.append(f"  ✅ {d} — COVERED")
    for d in uncovered:
        lines.append(f"  ⚠️ {d} — NOT COVERED")
    
    debuff_score = len(covered) / len(enemy_debuffs) * 100 if enemy_debuffs else 100
    lines.append(f"  Debuff Counter Score: {debuff_score:.0f}%")
    lines.append("")
    
    # 3. Leader Synergy
    lines.append("📊 3. LEADER SYNERGY:")
    leader = my_chars[0]
    filters = leader.get("leader_buff_filters", {})
    if filters:
        buffed = 0
        for mc in my_chars[1:]:
            type_match = mc["type"] in filters.get("types", [])
            class_match = bool(set(mc["classes"]) & set(filters.get("classes", [])))
            faction_match = bool(set(mc.get("factions", [])) & set(filters.get("factions", [])))
            if type_match or class_match or faction_match:
                buffed += 1
                lines.append(f"  ✅ #{mc['id']} {mc['name'][:30]} — receives leader buff")
            else:
                lines.append(f"  ❌ #{mc['id']} {mc['name'][:30]} — NO leader buff")
        synergy_pct = int(buffed / max(len(my_chars) - 1, 1) * 100)
    else:
        synergy_pct = 0
        lines.append("  ⚠️ Leader has no strong buff filters")
    lines.append(f"  Synergy Score: {synergy_pct}%")
    lines.append("")
    
    # 4. Special Interactions
    lines.append("📊 4. SPECIAL INTERACTIONS:")
    for mc in my_chars:
        # Check if unit specifically counters Five Elders
        if "Five Elders" in mc["tags"].get("counters", []):
            lines.append(f"  🔥 #{mc['id']} — ANTI-FIVE ELDERS specialist! (Forced Out to Five Elders)")
        # Check Bonney synergy
        if "bonney" in mc.get("special", "").lower():
            bonney_present = any("bonney" in CHARACTERS[tid]["name"].lower() for tid in team_ids if tid in CHARACTERS)
            if bonney_present:
                lines.append(f"  🔥 #{mc['id']} — Bonney synergy ACTIVATED!")
            else:
                lines.append(f"  ⚠️ #{mc['id']} — Has Bonney synergy but NO Bonney in team")
    lines.append("")
    
    # 5. Overall Score
    overall = min(100, max(0, 
        30 + type_score * 10 + debuff_score * 0.3 + synergy_pct * 0.3
    ))
    
    lines.append(f"{'='*60}")
    lines.append(f"OVERALL SCORE: {overall:.0f}/100")
    
    if overall >= 80:
        lines.append("🏆 EXCELLENT team plan! High chance of victory.")
    elif overall >= 60:
        lines.append("👍 GOOD team plan with some weaknesses.")
    elif overall >= 40:
        lines.append("⚠️ DECENT but has significant gaps.")
    else:
        lines.append("❌ WEAK team plan. Consider major changes.")
    
    my_team_str = " → ".join(f"#{c['id']} ({c['type']})" for c in my_chars)
    enemy_team_str = " → ".join(f"#{c['id']} ({c['type']})" for c in enemy_chars)
    lines.append(f"\nYOUR TEAM: {my_team_str}")
    lines.append(f"VS ENEMY: {enemy_team_str}")
    
    return "\n".join(lines)
