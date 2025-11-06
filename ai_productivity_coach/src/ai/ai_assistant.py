# import os
# import time
# try:
#     import openai
# except Exception:
#     openai = None

# OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
# if openai and OPENAI_KEY:
#     openai.api_key = OPENAI_KEY

# # Simple token-budgeting: estimate tokens per char (rough)
# def estimate_tokens(text: str) -> int:
#     return max(1, len(text) // 4)

# def trim_history_for_budget(history, max_tokens=2000):
#     # Keep system + most recent messages until token budget reached
#     if not history:
#         return history
#     total = 0
#     out = []
#     # always keep first system message if present
#     if history[0].get("role") == "system":
#         out.append(history[0])
#     # iterate backwards for recency
#     for msg in reversed(history[1:]):
#         t = estimate_tokens(msg.get("content", ""))
#         if total + t > max_tokens:
#             break
#         out.insert(1, msg)  # insert after system
#         total += t
#     return out

# class AIAssistant:
#     """
#     chat_with_history(history) -> (reply_text, meta_dict)
#     meta_dict may contain keys:
#       - create_task: string title
#       - start_timer: integer minutes
#     """

#     def suggest_breakdown(self, task_text: str) -> str:
#         # Basic reuse: call chat_with_history with a targeted prompt
#         prompt = f"Split the following task into 3-6 actionable subtasks with brief deadlines:\n\nTask: {task_text}\n\nSubtasks:"
#         return self._call_openai_simple(prompt) if openai and OPENAI_KEY else self._mock_breakdown(task_text)

#     def _mock_breakdown(self, text):
#         parts = []
#         words = text.split()
#         n = min(4, max(2, len(words) // 3))
#         for i in range(n):
#             parts.append(f"{i+1}. {text[:max(20, len(text)//n)]} — due in {2+i} days")
#         return "\n".join(parts)

#     def _call_openai_simple(self, prompt):
#         try:
#             resp = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": prompt}],
#                 max_tokens=400,
#                 temperature=0.3,
#             )
#             return resp["choices"][0]["message"]["content"].strip()
#         except Exception as e:
#             return f"(AI request failed) {e}"

#     def chat_with_history(self, history):
#         """
#         history: list of dicts {"role": "system"/"user"/"assistant", "content": "..."}
#         Returns (reply_text, meta_dict)
#         """
#         meta = {}

#         # Basic command parsing on last user message (fast local actions)
#         last_user = None
#         for m in reversed(history):
#             if m.get("role") == "user":
#                 last_user = m.get("content", "")
#                 break
#         if last_user:
#             lu = last_user.strip()
#             lower = lu.lower()
#             # quick local commands: "breakdown:", "create task:", "set timer:"
#             if lower.startswith("breakdown:"):
#                 task = lu.split(":", 1)[1].strip()
#                 return (self.suggest_breakdown(task), {})
#             if lower.startswith("create task:") or lower.startswith("add task:"):
#                 title = lu.split(":", 1)[1].strip()
#                 meta["create_task"] = title
#                 return (f"Created task: {title}", meta)
#             if lower.startswith("set timer:") or lower.startswith("start timer:"):
#                 rest = lu.split(":", 1)[1].strip().split()
#                 try:
#                     mins = int(rest[0])
#                     meta["start_timer"] = mins
#                     return (f"Starting a {mins}-minute timer.", meta)
#                 except Exception:
#                     return ("I didn't understand the timer length. Use: 'Set timer: 25' (minutes).", {})

#         # If OpenAI is available, call with trimmed history
#         if openai and OPENAI_KEY:
#             msgs = []
#             # Trim history to token budget to avoid errors
#             trimmed = trim_history_for_budget(history, max_tokens=1800)
#             for m in trimmed:
#                 msgs.append({"role": m.get("role"), "content": m.get("content")})
#             # Ensure there is a system message
#             if not any(m.get("role") == "system" for m in msgs):
#                 msgs.insert(0, {"role": "system", "content": "You are a concise, actionable AI productivity coach."})
#             try:
#                 resp = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=msgs,
#                     max_tokens=600,
#                     temperature=0.6,
#                 )
#                 text = resp["choices"][0]["message"]["content"].strip()
#                 # Optional: post-process for meta hints (very simple)
#                 # e.g., model can include lines like: [CREATE_TASK: title] or [START_TIMER: 25]
#                 if "[CREATE_TASK:" in text.upper():
#                     # parse first occurrence
#                     try:
#                         start = text.upper().index("[CREATE_TASK:")
#                         tail = text[start:].split("]", 1)[0]
#                         title = tail.split(":",1)[1].strip(" ]")
#                         meta["create_task"] = title
#                     except Exception:
#                         pass
#                 if "[START_TIMER:" in text.upper():
#                     try:
#                         start = text.upper().index("[START_TIMER:")
#                         tail = text[start:].split("]", 1)[0]
#                         mins = int(tail.split(":",1)[1].strip(" ]"))
#                         meta["start_timer"] = mins
#                     except Exception:
#                         pass
#                 return (text, meta)
#             except Exception as e:
#                 return (f"(AI request failed) {e}", {})

#         # Fallback simple responses if no OpenAI key
#         if last_user:
#             lower = last_user.lower()
#             if "timer" in lower or "pomodoro" in lower:
#                 return ("Try a 25-minute Pomodoro: focus for 25 minutes, then take a 5-minute break.", {})
#             if "priority" in lower:
#                 return ("Rank by urgency & impact. Mark 3 top-priority tasks for today.", {})
#             return ("I can help: 'Breakdown: <task>', 'Set timer: <minutes>', or 'Create task: <title>'.", {})
#         return ("Hello — what would you like help with?", {})






















import os
import time
import random

try:
    import openai
except Exception:
    openai = None

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY


# Simple token-budgeting
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def trim_history_for_budget(history, max_tokens=2000):
    if not history:
        return history
    total = 0
    out = []
    if history[0].get("role") == "system":
        out.append(history[0])
    for msg in reversed(history[1:]):
        t = estimate_tokens(msg.get("content", ""))
        if total + t > max_tokens:
            break
        out.insert(1, msg)
        total += t
    return out


class AIAssistant:
    """
    chat_with_history(history) -> (reply_text, meta_dict)
    meta_dict may contain keys:
      - create_task: string title
      - start_timer: integer minutes
    """

    # ---------------------------
    # 🌈 Helper + Personality
    # ---------------------------
    def _emoji(self, theme="neutral"):
        themes = {
            "motivate": ["💪", "🔥", "🚀", "✨", "🌟"],
            "focus": ["🎯", "🧘", "⏰", "📚", "🧠"],
            "neutral": ["💬", "🤖", "🙂"],
        }
        return random.choice(themes.get(theme, ["💬"]))

    def _motivate_quote(self):
        quotes = [
            "Small steps each day lead to big results! 💫",
            "Stay consistent — progress beats perfection 🚀",
            "Focus on the process, not just the outcome 🧘",
            "You’ve got this! Keep going 💪",
            "Take a short break and come back stronger ☕",
        ]
        return random.choice(quotes)

    # ---------------------------
    # 🔧 Core AI Logic
    # ---------------------------
    def suggest_breakdown(self, task_text: str) -> str:
        prompt = f"Break down this goal into clear steps with small deadlines:\n\nTask: {task_text}\n\nSubtasks:"
        return self._call_openai_simple(prompt) if openai and OPENAI_KEY else self._mock_breakdown(task_text)

    def _mock_breakdown(self, text):
        parts = []
        words = text.split()
        n = min(5, max(3, len(words) // 4))
        for i in range(n):
            parts.append(f"{i+1}. Complete part {i+1} of '{text}' — due in {1+i} days {self._emoji('focus')}")
        return "\n".join(parts) + f"\n\n{self._motivate_quote()}"

    def _call_openai_simple(self, prompt):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.4,
            )
            return resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"(AI request failed) {e}"

    # ---------------------------
    # 💬 Chat Interaction Logic
    # ---------------------------
    def chat_with_history(self, history):
        meta = {}
        last_user = None
        for m in reversed(history):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break

        if not last_user:
            return ("Hey 👋 I’m your productivity buddy. What’s your first goal for today?", {})

        lu = last_user.strip()
        lower = lu.lower()

        # -----------------------------
        # 🌞 Greetings and mood
        # -----------------------------
        if any(w in lower for w in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]):
            replies = [
                "Hey there! 🌟 Ready to make some progress today?",
                "Hello 👋 Let’s get productive — one step at a time!",
                "Hey! Hope you’re feeling motivated today 💪",
                "Hi there 🙂 What would you like to focus on first?"
            ]
            return (random.choice(replies), {})

        if any(w in lower for w in ["how are you", "how’s it going", "what’s up"]):
            replies = [
                "I’m all charged up ⚡ Ready to help you crush your goals!",
                "Feeling motivated as always 😎 How about you?",
                "Doing great! Let’s make today count 💫"
            ]
            return (random.choice(replies), {})

        # -----------------------------
        # 🎯 Focus, procrastination, and motivation
        # -----------------------------
        if any(w in lower for w in ["focus", "distracted", "procrastinate", "lazy", "can't concentrate", "lost focus"]):
            replies = [
                "Try a 25-minute deep-focus session ⏳ Then reward yourself with a 5-minute break!",
                "Block distractions for 20 minutes — just one focused sprint 🎯",
                "Start with one simple task. Once you begin, momentum takes over 🚀",
                "You don’t need motivation, just momentum 💡 Begin anywhere!"
            ]
            return (random.choice(replies), {})

        if any(w in lower for w in ["motivate", "inspire", "quote", "energy", "encourage"]):
            quotes = [
                "“Discipline beats motivation.” — keep showing up even when it’s hard 💪",
                "Every expert was once a beginner 🌱",
                "Progress, not perfection. Each step matters 🧭",
                "You’re stronger than your excuses 🚀",
                "Stay patient. Consistency turns small habits into huge success 🌟"
            ]
            return (random.choice(quotes), {})

        # -----------------------------
        # 📚 Study, learning, and work
        # -----------------------------
        if any(w in lower for w in ["study", "learn", "exam", "homework", "assignment"]):
            replies = [
                "Study tip 📘: Break topics into 25-minute chunks. Review, rest, repeat.",
                "Learning isn’t a sprint — it’s a marathon 🧠 Stay steady.",
                "Focus on understanding, not memorizing 💡",
                "Make a 3-task study plan for today — keep it small and doable 🎯"
            ]
            return (random.choice(replies), {})

        if any(w in lower for w in ["work", "project", "deadline", "job"]):
            replies = [
                "Break your work into 3 clear subtasks and start with the easiest one 🧩",
                "Deadlines are closer than they appear 😅 Start early!",
                "Remember: done is better than perfect ✅",
                "Stay consistent — progress adds up fast 🚀"
            ]
            return (random.choice(replies), {})

        # -----------------------------
        # 🌿 Stress, burnout, emotions
        # -----------------------------
        if any(w in lower for w in ["tired", "stressed", "anxious", "burnout", "angry", "upset", "sad"]):
            replies = [
                "Take a deep breath 🌿 You’re doing better than you think.",
                "It’s okay to pause. Rest is part of productivity ❤️",
                "You’re not alone — slow down, hydrate, breathe 🌼",
                "Don’t be too hard on yourself. You’re learning, growing, evolving 💫"
            ]
            return (random.choice(replies), {})

        if any(w in lower for w in ["overwhelmed", "too much work", "can’t handle", "pressure"]):
            replies = [
                "Let’s simplify things 🎯 Pick just ONE task for now.",
                "Write down all tasks and choose your top 3 priorities 🧘",
                "Remember — not everything needs to be done today 🌸",
                "Small steps over time beat big leaps in panic 💪"
            ]
            return (random.choice(replies), {})

        # -----------------------------
        # 💭 Confidence & setbacks
        # -----------------------------
        if any(w in lower for w in ["failed", "mistake", "not good enough", "can’t do"]):
            replies = [
                "Failure is feedback, not final 🚀",
                "Every mistake brings you one step closer to mastery 💡",
                "Be kind to yourself — progress isn’t always visible 🌱",
                "Success isn’t about never falling — it’s about rising every time 💪"
            ]
            return (random.choice(replies), {})

        # -----------------------------
        # 🕒 Planning & time management
        # -----------------------------
        if any(w in lower for w in ["plan", "schedule", "routine", "organize", "todo"]):
            replies = [
                "Here’s a trick: plan your top 3 tasks for the day 🗓️",
                "Start your day with one high-impact task ⚡",
                "Keep mornings for deep work, evenings for review 🧠",
                "A clear routine keeps you calm and productive 🌿"
            ]
            return (random.choice(replies), {})

        if lower.startswith(("set timer:", "start timer:")):
            rest = lu.split(":", 1)[1].strip().split()
            try:
                mins = int(rest[0])
                meta["start_timer"] = mins
                return (f"⏰ Timer set for {mins} minutes — let’s focus hard! {self._emoji('focus')}", meta)
            except Exception:
                return ("I couldn’t read the time. Try: `Set timer: 25` (minutes) ⏳", {})

        if lower.startswith(("create task:", "add task:")):
            title = lu.split(":", 1)[1].strip()
            meta["create_task"] = title
            return (f"✅ Task added: *{title}*\nLet's conquer it step by step 💪", meta)

        if lower.startswith("breakdown:"):
            task = lu.split(":", 1)[1].strip()
            reply = self.suggest_breakdown(task)
            return (f"Here’s your task plan 📋:\n\n{reply}", {})

        # -----------------------------
        # 🌙 End-of-day reflections
        # -----------------------------
        if any(w in lower for w in ["good night", "end my day", "see you", "bye", "sleep"]):
            replies = [
                "Good night 🌙 You did well today — rest and recharge.",
                "Logging off? Nice work today 👏 Sleep peacefully 🌼",
                "You earned your rest 😴 See you tomorrow for new wins!",
                "Day complete ✅ Reflect, relax, and sleep well 🌙"
            ]
            return (random.choice(replies), {})

        if any(w in lower for w in ["reflect", "journal", "learned", "improve", "lesson"]):
            replies = [
                "🧭 Reflection builds wisdom. What’s one thing you learned today?",
                "Write down 3 wins — even small ones — to celebrate 🎉",
                "Note one thing you could do 1% better tomorrow 🌱",
                "Reflection makes experience your best teacher 📖"
            ]
            return (random.choice(replies), {})

        # -----------------------------
        # Default fallback
        # -----------------------------
        fallback = [
            f"{self._emoji('neutral')} I can help you plan, stay focused, or relax your mind!",
            f"{self._emoji('neutral')} Need help breaking a big task into steps?",
            f"{self._emoji('neutral')} Want to start a Pomodoro focus timer?",
            f"{self._emoji('neutral')} Feeling stuck? I can help you refocus."
        ]
        return (random.choice(fallback) + "\n" + self._motivate_quote(), {})
