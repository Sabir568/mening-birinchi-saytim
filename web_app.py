import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars: Hyper-Drive", page_icon="⚡", layout="wide")

# --- 2. CSS STYLE ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #ffffff; font-family: 'Arial'; }
    .status-bar { background: rgba(0, 210, 255, 0.2); border: 2px solid #00ffcc; border-radius: 15px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; font-weight: bold; }
    .mega-ultra-card { background: linear-gradient(45deg, #ff0000, #ffcc00); border-radius: 15px; padding: 20px; text-align: center; border: 3px solid white; box-shadow: 0 0 20px gold; margin-bottom: 10px; }
    .brawler-card { background: #111; border: 1px solid #00ffcc; border-radius: 8px; padding: 10px; text-align: center; font-size: 14px; margin-bottom: 5px; }
    .pass-panel { background: #050505; border: 2px solid #6200ff; border-radius: 15px; padding: 15px; height: 500px; overflow-y: scroll; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLERS DATABASE (78 ta) ---
B_DB = [
    "Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", 
    "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", 
    "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", 
    "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", 
    "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", 
    "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"
]

# --- 4. SESSION STATE INITIALIZATION ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 100, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free'
    })

# --- 5. LOGIC FUNCTIONS ---
def open_box(cost, b_chance, box_name):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner(f"Открытие {box_name}..."):
            time.sleep(0.5)
            rand = random.random()
            if rand < b_chance:
                available = [b for b in B_DB if b not in st.session_state.inv]
                if available:
                    new_b = random.choice(available)
                    st.session_state.inv.append(new_b)
                    st.balloons(); st.success(f"🔥 НОВЫЙ БОЕЦ: {new_b}!")
                else:
                    st.session_state.gold += (cost * 2)
                    st.info("💰 Все бойцы собраны! Кэшбэк х2!")
            else:
                cashback = int(cost * 0.5)
                st.session_state.gold += cashback
                st.toast(f"📦 Пусто! Возврат: {cashback} 💰")
    else:
        st.error("Недостаточно золота!")

# --- 6. UI MAIN ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔱 BRAWL STARS: HYPER-DRIVE 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems:,}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies:,}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.3])

with c1:
    st.header("🏪 МАГАЗИН")
    
    # MEGA ULTRA BOX
    st.markdown("""
