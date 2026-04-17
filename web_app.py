import streamlit as st
import random
import time

# --- KONFIGURATSIYA ---
st.set_page_config(page_title="Brawl Stars Ultimate", page_icon="⭐", layout="wide")

# --- STYLING (Neon va Brawl Stars foni) ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1614036417651-efe591214972?q=80&w=2000");
        background-size: cover;
        color: white;
    }
    .main-lobby {
        background: rgba(0, 0, 0, 0.75);
        border: 5px solid #f1c40f;
        border-radius: 30px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .resource-bar {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 50px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        border: 2px solid #f1c40f;
    }
    .brawler-card {
        background: linear-gradient(180deg, #3498db, #2980b9);
        border-radius: 20px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        border: 3px solid #fff;
        transition: 0.3s;
    }
    .brawler-card:hover { transform: scale(1.05); }
    .box-img { width: 150px; cursor: pointer; transition: 0.5s; }
    .box-img:hover { transform: rotate(10deg) scale(1.1); }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN HOLATI (DATABASE) ---
if 'coins' not in st.session_state: st.session_state.coins = 500
if 'gems' not in st.session_state: st.session_state.gems = 50
if 'inventory' not in st.session_state: 
    st.session_state.inventory = [{"name": "Shelly", "rarity": "Начальный", "img": "https://cdn.fbsbx.com/v/t59.2708-21/116934898_320341775775434_4223280145828821035_n.gif?_nc_cat=102&ccb=1-7&_nc_sid=5f2048&_nc_ohc=f6tS2n6H7ZcAb7W_R5u&_nc_ht=cdn.fbsbx.com&oh=03_QeaH9XG8z7f7g&oe=66000000"}]
if 'msg' not in st.session_state: st.session_state.msg = ""

# BRAWLERLAR MA'LUMOTI
BRAWLERS_DB = {
    "El Primo": {"rarity": "Редкий", "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1eHRqZnd4eHJ6eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/hS6U6l2Yv7MDRp8h8j/giphy.gif"},
    "Colt": {"rarity": "Редкий", "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1eHRqZnd4eHJ6eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/f3v0YI1U6vD9r7v6Z6/giphy.gif"},
    "Leon": {"rarity": "Легендарный", "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1eHRqZnd4eHJ6eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/3o7TKMGVpE9L9v9K92/giphy.gif"},
    "Crow": {"rarity": "Легендарный", "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1eHRqZnd4eHJ6eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/3o7TKMGVpE9L9v9K92/giphy.gif"},
    "Mortis": {"rarity": "Мифический", "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1eHRqZnd4eHJ6eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/3o7TKMGVpE9L9v9K92/giphy.gif"}
}

# --- FUNKSIYALAR ---
def open_case(type):
    if type == "Mega":
        items = list(BRAWLERS_DB.keys())
        won = random.choice(items)
        if not any(b['name'] == won for b in st.session_state.inventory):
            st.session_state.inventory.append({"name": won, "rarity": BRAWLERS_DB[won]['rarity'], "img": BRAWLERS_DB[won]['img']})
            st.session_state.msg = f"🌟 ВАУ! ВЫ ВЫБИЛИ {won.upper()}!"
            st.balloons()
        else:
            st.session_state.coins += 500
            st.session_state.msg = f"Повторка {won}! Получено +500 монет."

# --- INTERFEYS ---
# Resurslar
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='resource-bar'>💰 {st.session_state.coins}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='resource-bar'>💎 {st.session_state.gems}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='resource-bar'>👤 {len(st.session_state.inventory)}/60</div>", unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("<div class='main-lobby'>", unsafe_allow_html=True)
    st.header("🛒 МАГАЗИН ЯЩИКОВ")
    
    b1, b2 = st.columns(2)
    with b1:
        st.image("https://raw.githubusercontent.com/A-Shox/Brawl_Images/main/big_box.png", width=150)
        if st.button("КРАСНЫЙ ЯЩИК (100 💰)"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                open_case("Big")
                st.rerun()
    with b2:
        st.image("https://raw.githubusercontent.com/A-Shox/Brawl_Images/main/mega_box.png", width=150)
        if st.button("МЕГА ЯЩИК (80 💎)"):
            if st.session_state.gems >= 80:
                st.session_state.gems -= 80
                open_case("Mega")
                st.rerun()
    
    if st.session_state.msg:
        st.warning(st.session_state.msg)
    
    st.write("---")
    if st.button("ИГРАТЬ (ЗАРАБОТАТЬ МОНЕТЫ) ⚔️", use_container_width=True):
        win = random.randint(20, 100)
        st.session_state.coins += win
        if random.random() < 0.1: st.session_state.gems += 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.header("🗄️ МОИ БОЙЦЫ")
    for b in st.session_state.inventory:
        with st.container():
            st.markdown(f"""
                <div class='brawler-card'>
                    <img src='{b['img']}' width='80'>
                    <h4>{b['name']}</h4>
                    <small>{b['rarity']}</small>
                </div>
            """, unsafe_allow_html=True)

# Reset
if st.sidebar.button("Удалить Аккаунт"):
    st.session_state.clear()
    st.rerun()
