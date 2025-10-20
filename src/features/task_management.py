# class TaskManagement:
#     def create_task(self, data):
#         print("Task created with data:", data)
#         return {"status": "success", "task": data}

tasks = []

def add_task(title):
    tasks.append({"title": title, "done": False})

def list_tasks():
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} [{status}]")

def mark_done(index):
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True

def demo():
    print("\n--- Task Management ---")
    add_task("Finish coding project")
    add_task("Read productivity book")
    list_tasks()
    mark_done(0)
    print("\nAfter marking first task done:")
    list_tasks()
