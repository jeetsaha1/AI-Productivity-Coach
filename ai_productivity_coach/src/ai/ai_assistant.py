import os
import time
try:
    import openai
except Exception:
    openai = None

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY

# Simple token-budgeting: estimate tokens per char (rough)
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def trim_history_for_budget(history, max_tokens=2000):
    # Keep system + most recent messages until token budget reached
    if not history:
        return history
    total = 0
    out = []
    # always keep first system message if present
    if history[0].get("role") == "system":
        out.append(history[0])
    # iterate backwards for recency
    for msg in reversed(history[1:]):
        t = estimate_tokens(msg.get("content", ""))
        if total + t > max_tokens:
            break
        out.insert(1, msg)  # insert after system
        total += t
    return out

class AIAssistant:
    """
    chat_with_history(history) -> (reply_text, meta_dict)
    meta_dict may contain keys:
      - create_task: string title
      - start_timer: integer minutes
    """

    def suggest_breakdown(self, task_text: str) -> str:
        # Basic reuse: call chat_with_history with a targeted prompt
        prompt = f"Split the following task into 3-6 actionable subtasks with brief deadlines:\n\nTask: {task_text}\n\nSubtasks:"
        return self._call_openai_simple(prompt) if openai and OPENAI_KEY else self._mock_breakdown(task_text)

    def _mock_breakdown(self, text):
        parts = []
        words = text.split()
        n = min(4, max(2, len(words) // 3))
        for i in range(n):
            parts.append(f"{i+1}. {text[:max(20, len(text)//n)]} — due in {2+i} days")
        return "\n".join(parts)

    def _call_openai_simple(self, prompt):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3,
            )
            return resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"(AI request failed) {e}"

    def chat_with_history(self, history):
        """
        history: list of dicts {"role": "system"/"user"/"assistant", "content": "..."}
        Returns (reply_text, meta_dict)
        """
        meta = {}

        # Basic command parsing on last user message (fast local actions)
        last_user = None
        for m in reversed(history):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break
        if last_user:
            lu = last_user.strip()
            lower = lu.lower()
            # quick local commands: "breakdown:", "create task:", "set timer:"
            if lower.startswith("breakdown:"):
                task = lu.split(":", 1)[1].strip()
                return (self.suggest_breakdown(task), {})
            if lower.startswith("create task:") or lower.startswith("add task:"):
                title = lu.split(":", 1)[1].strip()
                meta["create_task"] = title
                return (f"Created task: {title}", meta)
            if lower.startswith("set timer:") or lower.startswith("start timer:"):
                rest = lu.split(":", 1)[1].strip().split()
                try:
                    mins = int(rest[0])
                    meta["start_timer"] = mins
                    return (f"Starting a {mins}-minute timer.", meta)
                except Exception:
                    return ("I didn't understand the timer length. Use: 'Set timer: 25' (minutes).", {})

        # If OpenAI is available, call with trimmed history
        if openai and OPENAI_KEY:
            msgs = []
            # Trim history to token budget to avoid errors
            trimmed = trim_history_for_budget(history, max_tokens=1800)
            for m in trimmed:
                msgs.append({"role": m.get("role"), "content": m.get("content")})
            # Ensure there is a system message
            if not any(m.get("role") == "system" for m in msgs):
                msgs.insert(0, {"role": "system", "content": "You are a concise, actionable AI productivity coach."})
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=msgs,
                    max_tokens=600,
                    temperature=0.6,
                )
                text = resp["choices"][0]["message"]["content"].strip()
                # Optional: post-process for meta hints (very simple)
                # e.g., model can include lines like: [CREATE_TASK: title] or [START_TIMER: 25]
                if "[CREATE_TASK:" in text.upper():
                    # parse first occurrence
                    try:
                        start = text.upper().index("[CREATE_TASK:")
                        tail = text[start:].split("]", 1)[0]
                        title = tail.split(":",1)[1].strip(" ]")
                        meta["create_task"] = title
                    except Exception:
                        pass
                if "[START_TIMER:" in text.upper():
                    try:
                        start = text.upper().index("[START_TIMER:")
                        tail = text[start:].split("]", 1)[0]
                        mins = int(tail.split(":",1)[1].strip(" ]"))
                        meta["start_timer"] = mins
                    except Exception:
                        pass
                return (text, meta)
            except Exception as e:
                return (f"(AI request failed) {e}", {})

        # Fallback simple responses if no OpenAI key
        if last_user:
            lower = last_user.lower()
            if "timer" in lower or "pomodoro" in lower:
                return ("Try a 25-minute Pomodoro: focus for 25 minutes, then take a 5-minute break.", {})
            if "priority" in lower:
                return ("Rank by urgency & impact. Mark 3 top-priority tasks for today.", {})
            return ("I can help: 'Breakdown: <task>', 'Set timer: <minutes>', or 'Create task: <title>'.", {})
        return ("Hello — what would you like help with?", {})