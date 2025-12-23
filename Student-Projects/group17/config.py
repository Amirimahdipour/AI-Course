# config.py

# --- GROQ MODELS ---
AVAILABLE_MODELS = {
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
}

# --- SETTINGS OPTIONS ---
SUPPORTED_LANGUAGES = [
    "Auto",
    "English",
    "Persian",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Russian",
    "Arabic",
]

LENGTH_OPTIONS = {
    "Short (Bullets)": "very concise, using primarily bullet points",
    "Medium (Standard)": "a balanced summary, 1-2 paragraphs with key highlights",
    "Long (Detailed)": "a comprehensive detailed summary covering all aspects",
}

TONE_OPTIONS = {
    "Professional": "executive, neutral, and formal",
    "Casual": "friendly, relaxed, and easy to read",
    "ELI5": "simple, as if explaining to a 5-year-old",
}

CREATIVITY_LEVELS = {"Precise": 0.1, "Balanced": 0.5, "Creative": 0.8}

# --- DEFAULTS ---
DEFAULT_SETTINGS = {
    "model": "llama-3.3-70b-versatile",
    "language": "Auto",
    "length": "Medium (Standard)",
    "tone": "Professional",
    "creativity": "Balanced",
}

# --- UI BUTTONS ---
BTN_SETTINGS = "⚙️ Settings"
BTN_HELP = "❓ Help"
BTN_ABOUT = "ℹ️ About"

# --- MESSAGES ---
HELP_TEXT = """
<b>❓ How to use this bot:</b>

1. <b>Send Text:</b> Paste any article, email, or document text here.
2. <b>Wait:</b> I will process and summarize it for you.
3. <b>Settings:</b> Use the menu to change the AI Model, Language, Tone, or Length.
"""

ABOUT_TEXT = """
<b>ℹ️ About</b>

This is a smart AI Summarizer Bot powered by <b>Groq</b>.
It uses advanced LLMs to distill complex information into clear summaries.

<b>Features:</b>
• Professional Text Summarization
• Multilingual Support
• Customizable Tone & Length
"""

# --- PROMPT ENGINEERING ---
SYSTEM_PROMPT_TEMPLATE = """
You are an expert summarizer acting in a {tone} capacity.

**Your Goal:**
Summarize the user's input text. The summary must be {length_instruction}.

**Formatting Guidelines (CRITICAL):**
1. You must format the output using **HTML** tags supported by Telegram.
2. Use <b>text</b> for bolding (e.g., for headers or key points).
3. Do NOT use Markdown (like **bold** or # header).
4. Do NOT use HTML tags like <br>, <p>, or <div>. Use newlines for spacing.

**Language:**
{language_instruction}
"""
