import json
import streamlit as st

from diet_logic import UserProfile, generate_week_plan
from utils import save_plan
from ai import explain_plan_fa, swap_meal_suggestion_fa

st.set_page_config(page_title="DietBot", page_icon="🥗")

st.title("DietBot — برنامه‌ریز غذایی ")

MEAL_FA = {
    "breakfast": "صبحانه",
    "lunch": "ناهار",
    "dinner": "شام",
    "snack": "میان‌وعده",
}

# ---------- Sidebar inputs ----------
with st.sidebar:
    st.header("اطلاعات کاربر")

    age = st.number_input("سن", min_value=10, max_value=90, value=29)
    gender_fa = st.selectbox("جنسیت", ["مرد", "زن"])
    height_cm = st.number_input("قد (سانتی‌متر)", min_value=120.0, max_value=220.0, value=180.0)
    weight_kg = st.number_input("وزن (کیلوگرم)", min_value=30.0, max_value=200.0, value=80.0)

    activity_fa = st.selectbox("سطح فعالیت", ["کم", "متوسط", "زیاد"])
    goal_fa = st.selectbox("هدف", ["کاهش وزن", "حفظ وزن", "افزایش وزن"])
    meals = st.selectbox("تعداد وعده در روز", [3, 4, 5], index=1)

def map_inputs():
    gender = "male" if gender_fa == "مرد" else "female"
    activity = {"کم": "low", "متوسط": "medium", "زیاد": "high"}[activity_fa]
    goal = {"کاهش وزن": "lose", "حفظ وزن": "maintain", "افزایش وزن": "gain"}[goal_fa]
    return gender, activity, goal

gender, activity, goal = map_inputs()

profile = UserProfile(
    age=int(age),
    gender=gender,
    height_cm=float(height_cm),
    weight_kg=float(weight_kg),
    activity=activity,
    goal=goal,
    meals_per_day=int(meals),
)

profile_dict = {
    "سن": int(age),
    "جنسیت": gender_fa,
    "قد": float(height_cm),
    "وزن": float(weight_kg),
    "فعالیت": activity_fa,
    "هدف": goal_fa,
    "تعداد وعده": int(meals),
}

# ---------- Generate plan button ----------
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("✅ ساخت برنامه غذایی ۷ روزه", use_container_width=True):
        plan = generate_week_plan(profile)
        st.session_state["plan"] = plan
        st.session_state["profile_dict"] = profile_dict

with col2:
    if st.button("🗑️ پاک کردن برنامه", use_container_width=True):
        st.session_state.pop("plan", None)
        st.session_state.pop("profile_dict", None)

# ---------- If plan exists, show it ----------
plan = st.session_state.get("plan")
saved_profile = st.session_state.get("profile_dict")

if plan:
    st.success(f"کالری هدف روزانه (تقریبی): {plan['kcal_target']} کیلوکالری")

    # --- ai Section ---
    st.subheader("🤖 بخش هوشمند ai ")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("💡 توضیح بده این برنامه چطوره؟", use_container_width=True):
            with st.spinner("در حال تولید توضیح..."):
                txt = explain_plan_fa(saved_profile, plan)
            st.write(txt)

    with c2:
        day_index = st.number_input("شماره روز (۱ تا ۷)", min_value=1, max_value=7, value=1)
        meal_choice = st.selectbox("کدام وعده؟", ["صبحانه", "ناهار", "شام", "میان‌وعده"])
        if st.button("✨ 3 جایگزین پیشنهاد بده", use_container_width=True):
            with st.spinner("در حال تولید جایگزین‌ها..."):
                day = plan["days"][int(day_index) - 1]
                sug = swap_meal_suggestion_fa(day, meal_choice)
            st.write(sug)

    st.divider()

    # --- Show weekly plan ---
    for i, day in enumerate(plan["days"], start=1):
        st.subheader(f"روز {i}")

        rows = []
        for m in day["meals"]:
            rows.append({
                "وعده": MEAL_FA.get(m["type"], m["type"]),
                "غذا": m["name"],
                "کالری": m["kcal"],
            })

        st.table(rows)
        st.write(f"جمع کالری این روز: **{day['total_kcal']}** (هدف: {day['target_kcal']})")
        st.divider()

    # --- Save + download ---
    path = save_plan(plan)
    st.info(f"برنامه در فایل ذخیره شد: {path}")

    st.download_button(
        label="⬇️ دانلود خروجی JSON",
        data=json.dumps(plan, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="diet_plan.json",
        mime="application/json",
    )

else:
    st.info("برای شروع، از بالا روی «ساخت برنامه غذایی ۷ روزه» کلیک کن.")
