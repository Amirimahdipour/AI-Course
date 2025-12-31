import os
import json
from typing import Dict, Any, Optional

# --- OpenAI optional ---
try:
    import streamlit as st
except Exception:
    st = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# --- Ollama local ---
import urllib.request


def _get_key() -> Optional[str]:
    if st is not None:
        try:
            k = st.secrets.get("OPENAI_API_KEY")
            if k:
                return str(k)
        except Exception:
            pass
    k = os.getenv("OPENAI_API_KEY")
    return k if k else None


def _openai_client() -> Optional["OpenAI"]:
    if OpenAI is None:
        return None
    key = _get_key()
    if not key:
        return None
    return OpenAI(api_key=key)


def _ollama_generate(prompt: str, model: str = "llama3") -> str:
    """
    Call local Ollama server: http://localhost:11434/api/generate
    """
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    return out.get("response", "").strip()


def _safe_text(err: Exception) -> str:
    return f"❌ خطا: {type(err).__name__} — {err}"


def explain_plan_fa(profile: Dict[str, Any], plan: Dict[str, Any]) -> str:
    prompt = f"""
تو یک دستیار آموزشی هستی (نه پزشک).
به زبان فارسی خیلی ساده توضیح بده:
1) این برنامه برای هدف کاربر به طور کلی مناسب هست یا نه (آموزشی)
2) 3 پیشنهاد برای بهتر شدن (آب، پروتئین، سبزیجات، خواب، پیاده‌روی…)
3) اگر کاربر گرسنه شد، 3 میان‌وعده سالم پیشنهاد بده
قوانین:
- نسخه پزشکی نده
- کوتاه و قابل فهم (حداکثر 12 خط)

اطلاعات کاربر:
{profile}

برنامه:
{plan}
""".strip()

    # 1) try OpenAI
    client = _openai_client()
    if client is not None:
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Educational nutrition helper. No medical advice."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            # fallback to ollama
            pass

    # 2) fallback Ollama
    try:
        return _ollama_generate(prompt)
    except Exception as e:
        return "❌ KI فعال نیست. (نه OpenAI quota داری، نه Ollama اجرا شده)\n" + _safe_text(e)


def swap_meal_suggestion_fa(day_plan: Dict[str, Any], meal_type_fa: str) -> str:
    prompt = f"""
تو یک دستیار آموزشی تغذیه هستی.
برای وعده «{meal_type_fa}» در برنامه زیر، 3 جایگزین ساده پیشنهاد بده.
- غذاها ساده و در دسترس باشند
- کالری تقریبی هر جایگزین را هم بنویس (تخمینی)
- نسخه پزشکی نده، کوتاه جواب بده

روز برنامه:
{day_plan}
""".strip()

    # 1) try OpenAI
    client = _openai_client()
    if client is not None:
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Educational nutrition helper. No medical advice."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            pass

    # 2) fallback Ollama
    try:
        return _ollama_generate(prompt)
    except Exception as e:
        return "❌ KI فعال نیست. (Ollama اجرا نشده یا مدل نصب نیست)\n" + _safe_text(e)
