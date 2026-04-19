import sys
import json
import random

def generate_variant_question(key_point: str) -> dict:
    """
    生成变因题：如果变量X变化10倍，会发生什么
    """
    return {
        "type": "variant",
        "question": f"如果上述场景中的关键变量增加10倍，'{key_point}' 这个理论还成立吗？为什么？",
        "hint": "考虑边界条件和极限情况"
    }

def generate_trap_question(key_point: str) -> dict:
    """
    生成陷阱题：给出一个看似合理但错误的推论
    """
    traps = [
        f"既然'{key_point}'是对的，那么它的相反命题也一定是对的，对吗？",
        f"'{key_point}' 在所有场景下都适用吗？",
        f"如果把这个逻辑反过来推导，会得到什么结论？"
    ]
    return {
        "type": "trap",
        "question": random.choice(traps),
        "hint": "注意逻辑方向性和充分必要条件"
    }

def generate_comprehensive_question(key_points: list) -> dict:
    """
    生成综合题：结合多个知识点
    """
    if len(key_points) < 2:
        return None
    return {
        "type": "comprehensive",
        "question": f"如何结合 '{key_points[0]}' 和 '{key_points[1]}' 来解决实际问题？",
        "hint": "寻找两个知识点之间的关联"
    }

def generate_quiz(key_points: list, count: int = 3) -> dict:
    """
    生成测验题组
    """
    quizzes = []

    for kp in key_points[:count]:
        q_type = random.choice(["variant", "trap"])
        if q_type == "variant":
            quizzes.append(generate_variant_question(kp.get("content", "")))
        else:
            quizzes.append(generate_trap_question(kp.get("content", "")))

    if len(key_points) >= 2:
        comp = generate_comprehensive_question([point.get("content", "") for point in key_points[:2]])
        if comp:
            quizzes.append(comp)

    return {
        "status": "success",
        "count": len(quizzes),
        "quizzes": quizzes,
        "reward": {
            "correct": 50,
            "streak_bonus": 100
        }
    }

def load_key_points(file_path: str) -> list:
    """
    从extract.py的输出加载重点
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("key_points", [])
    except Exception as e:
        return []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key_points = load_key_points(sys.argv[1])
    else:
        key_points = [
            {"id": 1, "title": "要点1", "content": "分布式一致性的基础原理"},
            {"id": 2, "title": "要点2", "content": "Paxos算法的核心机制"}
        ]

    result = generate_quiz(key_points)
    print(json.dumps(result, ensure_ascii=False, indent=2))