from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import asyncio

app = FastAPI(title="AI Productivity Coach API")

# ✅ Allow requests from all origins (frontend can connect easily)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Data Model ----
class ChatRequest(BaseModel):
    message: str


# ---- Root Health Check ----
@app.get("/")
def root():
    return {"status": "ok"}


# ---- Helper: Random motivational quotes ----
QUOTES = [
    "“Discipline is doing what needs to be done, even when you don’t feel like it.” 💪",
    "“Focus on progress, not perfection.” ✨",
    "“The secret of getting ahead is getting started.” — Mark Twain 🚀",
    "“You don’t need more time, you just need more focus.” ⏳",
    "“Consistency beats intensity.” 🔥"
]


# ---- Core Chat Endpoint ----
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    user_message = req.message.lower().strip()

    # Small natural delay to simulate "thinking"
    await asyncio.sleep(random.uniform(1.2, 2.2))

    # --- Keyword groups ---
    greeting = ["hi", "hello", "hey", "good morning", "good evening"]
    focus_words = ["focus", "concentrate", "distraction"]
    plan_words = ["plan", "schedule", "task", "todo", "organize"]
    motivation_words = ["lazy", "procrastinate", "motivate", "inspire", "energy"]
    stress_words = ["stress", "tired", "burnout", "pressure", "anxious"]
    goal_words = ["goal", "target", "objective", "achievement", "dream"]
    thanks_words = ["thank", "thanks", "appreciate"]

    # --- Dynamic responses ---
    if any(word in user_message for word in greeting):
        reply = random.choice([
            "Hey there 👋! Let’s make today your most productive one yet.",
            "Hello! I’m your AI Productivity Coach — what’s your main goal today?",
            "Hi 👋 Ready to organize your thoughts and get some real progress done?"
        ])
    elif any(word in user_message for word in focus_words):
        reply = random.choice([
            "Try working in 25-minute focus blocks — your brain loves short sprints.",
            "Distractions kill momentum. How about a 30-minute deep work session?",
            "Close your tabs and set a timer — one focused task at a time 💡"
        ])
    elif any(word in user_message for word in plan_words):
        reply = random.choice([
            "Let’s plan your day around 3 key priorities — clarity beats chaos.",
            "Write your top task first thing — it sets a productive tone for the day.",
            "A structured to-do list clears your mental clutter instantly ✍️"
        ])
    elif any(word in user_message for word in motivation_words):
        reply = random.choice([
            "Remember — action creates motivation, not the other way around. Start small!",
            "Every tiny step compounds into big wins. You’ve got this 💪",
            "Feeling lazy? Just start for 2 minutes — momentum will follow 🔥"
        ])
    elif any(word in user_message for word in stress_words):
        reply = random.choice([
            "Take a deep breath. Productivity means balance too 🧘",
            "Your mind needs recovery to perform. Take a short mindful break ☕",
            "Let’s declutter what’s overwhelming you — one issue at a time 💭"
        ])
    elif any(word in user_message for word in goal_words):
        reply = random.choice([
            "Big goals? Perfect. Let’s break them into small weekly wins 🚀",
            "Dream big but plan smart — what’s your next small step?",
            "Focus on the next 1% improvement each day, and success compounds 💫"
        ])
    elif any(word in user_message for word in thanks_words):
        reply = random.choice([
            "Always here to help 😊 Keep building momentum!",
            "Glad I could assist — consistency will take you far!",
            "Anytime! Stay focused, you’re on the right path 💪"
        ])
    else:
        reply = random.choice([
            "Got it — want me to help you structure that into an actionable plan?",
            "Interesting thought 💡 How can we turn that into a productive next step?",
            "That’s valid — would you like a quick framework to approach it?",
            "I like your energy! Let’s channel that into something measurable ⚡",
            random.choice(QUOTES)
        ])

    return {"reply": reply}
