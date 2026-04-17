import streamlit as st
import random
import time

# --- SETUP ---
st.set_page_config(page_title="Brawl Stars ULTRA MAX", page_icon="🔥", layout="wide")

# --- ULTRA DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000428 0%, #004e92 100%);
        color: white;
    }
    .brawler-card {
        padding: 20px; border-radius: 25px; margin-bottom: 15px;
        text-align: center; border: 3px solid; transition: 0.3s;
    }
    .common { border-color: #3498db; background: rgba(52, 152, 219, 0.2); }
    .rare { border-color: #2ecc71; background: rgba(46, 204, 113, 0.2); }
    .epic { border-color: #9b59b6; background: rgba(155, 89, 182, 0.2); }
    .mythic { border-color: #e74c3c; background: rgba(231, 76, 60, 0.2); }
    .legendary { border-color: #f1c40f; background: rgba(241, 196, 15, 0.2); box-shadow: 0 0 15px #f1c40f; }
    
    .status-container {
        display: flex; justify-content: space-around;
        background: rgba(0,0,0,0.5); padding: 15px; border-radius: 50px;
        border: 2px solid #FFD700; margin-bottom: 25px;
    }
    .game-log {
        background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px;
        font-family: monospace; color: #00ff00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE & LOGIC ---
if 'coins' not in st.session_state: st.session_state.coins = 1000
if 'gems' not in st.session_state: st.session_state.gems = 100
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'inv' not in st.session_state: 
    st.session_state.inv = {"Shelly": {"level": 1, "power": 100, "rarity": "common"}}
if 'logs' not in st.session_state: st.session_state.logs = ["Добро пожаловать в Brawl Stars Ultra!"]

BRAWLERS_POOL = {
    "El Primo": "rare", "Colt": "rare", "Poco": "rare",
    "Piper": "epic", "Frank": "epic", "Bibi": "epic",
    "Mortis": "mythic", "Tara": "mythic", "Gene": "mythic",
    "Leon": "legendary", "Crow": "legendary", "Spike": "legendary", "Sandy": "legendary"
}

# --- FUNCTIONS ---
def add_log(text):
    st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] {text}")

def simulate_match():
    total_power = sum(b['power'] for b in st.session_state.inv.values())
    luck = random.randint(1, 100)
    if luck < 60: # 60% g'alaba ehtimoli
        win_t = random.randint(8, 12)
        win_c = random.randint(20, 50)
        st.session_state.trophies += win_t
        st.session_state.coins += win_c
        add_log(f"ПОБЕДА! +{win_t}🏆 +{win_c}💰")
        st.balloons()
    else:
        loss_t = random.randint(3, 6)
        st.session_state.trophies = max(0, st.session_state.trophies - loss_t)
        add_log(f"ПОРАЖЕНИЕ! -{loss_t}🏆")

def open_mega_box():
    if st.session_state.gems >= 80:
        st.session_state.gems -= 80
        if random.random() < 0.45: # 45% yangi brawler
            new_b = random.choice(list(BRAWLERS_POOL.keys()))
            if new_b not in st.session_state.inv:
                rarity = BRAWLERS_POOL[new_b]
                st.session_state.inv[new_b] = {"level": 1, "power": random.randint(150, 400), "rarity": rarity}
                add_log(f"🔥 ЛЕГЕНДАРНО! ВЫБИТ {new_b.upper()}!")
            else:
                bonus = 1000
                st.session_state.coins += bonus
                add_log(f"Дубликат {new_b}: +{bonus}💰")
        else:
            coins = random.randint(400, 800)
            st.session_state.coins += coins
            add_log(f"Мега-ящик: +{coins}💰")
    else:
        st.error("Недостаточно гемов!")

# --- UI DISPLAY ---
st.markdown(f"""
    <div class='status-container'>
        <span>💰 {st.session_state.coins}</span>
        <span>💎 {st.session_state.gems}</span>
        <span>🏆 {st.session_state.trophies}</span>
        <span>👤 {len(st.session_state.inv)} Бравлеров</span>
    </div>
    """, unsafe_allow_html=True)

col_main, col_side = st.columns([2, 1])

with col_main:
    st.header("🎮 Battle Zone")
    if st.button("🚀 НАЧАТЬ МАТЧ (PLAY)", use_container_width=True):
        simulate_match()
        st.rerun()
    
    st.write("---")
    st.header("🛍️ Shop & Boxes")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("### 🎁 Big Box")
        if st.button("300 💰"):
            if st.session_state.coins >= 300:
                st.session_state.coins -= 300
                open_mega_box() # Funksiya ichida mantiq bir xil
                st.rerun()
    with s2:
        st.markdown("### 🔵 Mega Box")
        if st.button("80 💎"):
            open_mega_box()
            st.rerun()

    st.write("---")
    st.subheader("📝 Game Logs")
    for log in st.session_state.logs[:5]:
        st.markdown(f"<div class='game-log'>{log}</div>", unsafe_allow_html=True)

with col_side:
    st.header("👥 Your Brawlers")
    for name, data in st.session_state.inv.items():
        st.markdown(f"""
            <div class='brawler-card {data['rarity']}'>
                <h3 style='margin:0;'>{name}</h3>
                <p>{data['rarity'].upper()}</p>
                <p><b>LVL {data['level']}</b> | PWR {data['power']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        up_cost = data['level'] * 500
        if st.button(f"UPGRADE ({up_cost}💰)", key=f"up_{name}"):
            if st.session_state.coins >= up_cost:
                st.session_state.coins -= up_cost
                st.session_state.inv[name]['level'] += 1
                st.session_state.inv[name]['power'] += 50
                st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Profile")
    st.write(f"Trophy Road: {st.session_state.trophies}/50000")
    st.progress(min(st.session_state.trophies / 5000, 1.0))
    if st.button("Reset Account"):
        st.session_state.clear()
        st.rerun()
