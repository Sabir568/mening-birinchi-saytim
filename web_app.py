import streamlit as st
import random
import time

# Конфигурация
st.set_page_config(page_title="Brawl Stars Case Simulator", page_icon="⭐", layout="wide")

# --- СТИЛЬ BRAWL STARS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e90ff, #1c1c1c);
        color: #ffffff;
    }
    .lobby-card {
        background: rgba(0, 0, 0, 0.6);
        border: 4px solid #f1c40f;
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(241, 196, 15, 0.4);
    }
    .resource-text {
        font-size: 24px;
        font-weight: bold;
        color: #f1c40f;
        text-shadow: 2px 2px 5px #000;
    }
    .brawler-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 5px;
        border: 1px solid #555;
        text-align: left;
    }
    .box-btn {
        transition: 0.3s;
    }
    .box-btn:hover {
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ---
if 'coins' not in st.session_state: st.session_state.coins = 100
if 'gems' not in st.session_state: st.session_state.gems = 10
if 'brawlers' not in st.session_state: st.session_state.brawlers = ["Shelly"]
if 'last_reward' not in st.session_state: st.session_state.last_reward = ""

# Данные о ящиках
BOXES = {
    "Brawl Box": {"cost": 50, "gems_cost": 0, "img": "📦", "luck": ["El Primo", "Barley", "Poco", "Rosa"]},
    "Big Box": {"cost": 200, "gems_cost": 0, "img": "🎁", "luck": ["Colt", "Bull", "Jessie", "Brock", "Dynamike"]},
    "Mega Box": {"cost": 0, "gems_cost": 40, "img": "🔵", "luck": ["Piper", "Pam", "Frank", "Bibi", "Mortis", "Leon", "Crow", "Spike"]}
}

# --- ФУНКЦИЯ ОТКРЫТИЯ ---
def open_box(box_name):
    box = BOXES[box_name]
    if random.random() < 0.3: # 30% шанс на нового бравлера
        new_brawler = random.choice(box["luck"])
        if new_brawler not in st.session_state.brawlers:
            st.session_state.brawlers.append(new_brawler)
            st.session_state.last_reward = f"НОВЫЙ БРАВЛЕР: {new_brawler}! 🎉"
            st.balloons()
        else:
            bonus_coins = random.randint(50, 150)
            st.session_state.coins += bonus_coins
            st.session_state.last_reward = f"Повторка {new_brawler}! Дали {bonus_coins} монет."
    else:
        bonus_coins = random.randint(20, 80)
        st.session_state.coins += bonus_coins
        st.session_state.last_reward = f"Выпало {bonus_coins} монет."

# --- ЛОББИ ---
st.title("⭐ Brawl Stars: Lobby & Case Simulator")

# Панель ресурсов
res_col1, res_col2, res_col3 = st.columns(3)
with res_col1: st.markdown(f"<div class='resource-text'>💰 Монеты: {st.session_state.coins}</div>", unsafe_allow_html=True)
with res_col2: st.markdown(f"<div class='resource-text'>💎 Гемы: {st.session_state.gems}</div>", unsafe_allow_html=True)
with res_col3: st.markdown(f"<div class='resource-text'>👤 Бойцы: {len(st.session_state.brawlers)}</div>", unsafe_allow_html=True)

st.write("---")

col_main, col_inv = st.columns([2, 1])

# --- ЦЕНТРАЛЬНОЕ ЛОББИ ---
with col_main:
    st.markdown("<div class='lobby-card'>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1614036417651-efe591214972?w=500", caption="Brawl Stars Lobby")
    st.write("### 🎁 Магазин ящиков")
    
    b1, b2, b3 = st.columns(3)
    
    with b1:
        st.write("📦 **Brawl Box**")
        if st.button("Открыть (50 💰)", key="b1"):
            if st.session_state.coins >= 50:
                st.session_state.coins -= 50
                open_box("Brawl Box")
                st.rerun()
            else: st.error("Мало монет!")
            
    with b2:
        st.write("🎁 **Big Box**")
        if st.button("Открыть (200 💰)", key="b2"):
            if st.session_state.coins >= 200:
                st.session_state.coins -= 200
                open_box("Big Box")
                st.rerun()
            else: st.error("Мало монет!")

    with b3:
        st.write("🔵 **Mega Box**")
        if st.button("Открыть (40 💎)", key="b3"):
            if st.session_state.gems >= 40:
                st.session_state.gems -= 40
                open_box("Mega Box")
                st.rerun()
            else: st.error("Мало гемов!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.last_reward:
        st.info(st.session_state.last_reward)

    # Кнопка заработка
    st.write("---")
    if st.button("КЛИКАТЬ ДЛЯ ПОЛУЧЕНИЯ МОНЕТ ⚡", use_container_width=True):
        st.session_state.coins += 10
        if random.random() < 0.05: st.session_state.gems += 1
        st.rerun()

# --- СПИСОК БОЙЦОВ ---
with col_inv:
    st.header("👤 Мои Бойцы")
    for b in st.session_state.brawlers:
        st.markdown(f"<div class='brawler-card'>⭐ {b}</div>", unsafe_allow_html=True)

# Сброс
if st.sidebar.button("Сбросить аккаунт"):
    st.session_state.clear()
    st.rerun()
