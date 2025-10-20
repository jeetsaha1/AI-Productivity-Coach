# class AIPrioritization:
#     pass

def rank_tasks(tasks):
    # Fake ranking: sort alphabetically
    return sorted(tasks, key=lambda x: x["title"])

def demo():
    print("\n--- AI Prioritization ---")
    sample = [{"title": "Do homework"}, {"title": "Check emails"}, {"title": "Exercise"}]
    ranked = rank_tasks(sample)
    print("Ranked tasks:")
    for t in ranked:
        print("-", t["title"])
