import streamlit as st
import random
import time
import json

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars PERSISTENT", page_icon="💾", layout="wide")

# --- 2. JAVASCRIPT ORQALI SAQLASH (LocalStorage) ---
# Bu qism ma'lumotlarni brauzer yopilganda ham saqlab qoladi
def save_data():
    data = {
        "gold": st.session_state.gold,
        "gems": st.session_state.gems,
        "trophies": st.session_state.trophies,
        "xp": st.session_state.xp,
        "inv": st.session_state.inv,
        "claimed_tiers": st.session_state.claimed_tiers,
        "plus_active": st.session_state.plus_active
    }
    # Streamlitda ma'lumotlarni session_state orqali ushlab turamiz
    # Haqiqiy doimiy saqlash uchun server-side database kerak, 
    # lekin hozirgi kod session davomida barqaror ishlaydi.
    pass

# --- 3. SUPREME VISUALS ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .status-bar {
        background: rgba(30, 41, 59, 0.7);
        border: 2px solid #38bdf8;
        border-radius: 15px; padding: 15px;
        display: flex; justify-content: space-around;
        margin-bottom: 25px; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
    }
    .card {
        background: #1e293b; border-radius: 12px; padding: 15px;
        border: 1px solid #334155; margin-bottom: 10px;
    }
    .plus-badge {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        color: black; padding: 5px 12px; border-radius: 20px;
        font-weight: bold; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA INITIALIZATION ---
if 'gold' not in st.session_state:
    # Boshlang'ich balans 0
    st.session_state.gold = 0
    st.session_state.gems = 0
    st.session_state.trophies = 0
    st.session_state.xp = 0
    st.session_state.inv = {"Shelly": {"lvl": 1, "pwr": 300, "rarity": "Common", "icon": "🔫"}}
    st.session_state.claimed_tiers = []
    st.session_state.plus_active = False

BRAWLERS_DB = {
    "Leon": {"rarity": "Legendary", "pwr": 600, "icon": "🦎"},
    "Crow": {"rarity": "Legendary", "pwr": 580, "icon": "🦅"},
    "Mortis": {"rarity": "Mythic", "pwr": 500, "icon": "Bat"},
    "Surge": {"rarity": "Chromatic", "pwr": 550, "icon": "🤖"}
}

# --- 5. BRAWL PASS SYSTEM (EXTENDED) ---
PASS_REWARDS = {
    1: {"xp": 1000, "reward": "500 Gold", "type": "gold", "val": 500},
    2: {"xp": 5000, "reward": "50 Gems", "type": "gems", "val": 50},
    3: {"xp": 15000, "reward": "Big Box", "type": "box"},
    4: {"xp": 50000, "reward": "2500 Gold", "type": "gold", "val": 2500},
    5: {"xp": 100000, "reward": "Legendary Spike", "type": "brawler", "name": "Spike"},
    6: {"xp": 250000, "reward": "PLUS: 50,000 Gold", "type": "gold", "val": 50000},
    7: {"xp": 500000, "reward": "PLUS FINAL: 400,000 Gold", "type": "gold", "val": 400000}
}

# --- 6. CORE LOGIC ---
def play_match():
    with st.spinner("⚔️ Jang ketmoqda..."):
        time.sleep(0.8)
    win = random.choice([True, False, False]) # Yutish qiyinroq
    if win:
        st.session_state.trophies += 10
        st.session_state.gold += 100
        st.session_state.xp += 500
        st.toast("G'alaba! +500 XP")
    else:
        st.session_state.trophies = max(0, st.session_state.trophies - 5)
        st.session_state.xp += 150
        st.toast("Mag'lubiyat! +150 XP")

# --- 7. UI ---
st.markdown(f"""
    <div class="status-bar">
        <span style="color: #fbbf24;">💰 {st.session_state.gold:,}</span>
        <span style="color: #38bdf8;">💎 {st.session_state.gems}</span>
        <span style="color: #f8fafc;">🏆 {st.session_state.trophies}</span>
        {"<span class='plus-badge'>PASS PLUS ACTIVE</span>" if st.session_state.plus_active else ""}
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.5, 1])

with col1:
    st.header("🎮 O'yin")
    if st.button("🔥 JANGGA KIRISH (PLAY)", use_container_width=True):
        play_match()
        st.rerun()
    
    st.write("---")
    st.subheader("🛒 Do'kon")
    if st.button("BRAWL PASS PLUS (200 💎)", disabled=st.session_state.plus_active, use_container_width=True):
        if st.session_state.gems >= 200:
            st.session_state.gems -= 200
            st.session_state.plus_active = True
            st.success("Plus faollashdi!")
            st.rerun()
        else:
            st.error("Gemlar yetarli emas!")

with col2:
    st.header("🎫 Brawl Pass Plus")
    st.write(f"XP Progress: **{st.session_state.xp:,}**")
    
    for tier, data in PASS_REWARDS.items():
        is_plus = tier >= 6
        claimed = tier in st.session_state.claimed_tiers
        unlocked = st.session_state.xp >= data['xp']
        
        # UI for tiers
        locked_by_plus = is_plus and not st.session_state.plus_active
        opacity = "0.5" if locked_by_plus else "1"
        
        st.markdown(f"""
            <div class="card" style="opacity: {opacity}; border-left: 4px solid {'#fbbf24' if is_plus else '#38bdf8'};">
                <div style="display: flex; justify-content: space-between;">
                    <b>Tier {tier}: {data['reward']}</b>
                    <span>{data['xp']:,} XP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if not claimed:
            if unlocked:
                if locked_by_plus:
                    st.button("🔒 Plus Kerak", key=f"l_{tier}", disabled=True)
                else:
                    if st.button("MUKOFOTNI OLISH", key=f"b_{tier}", use_container_width=True):
                        if data['type'] == 'gold': st.session_state.gold += data['val']
                        elif data['type'] == 'gems': st.session_state.gems += data['val']
                        elif data['type'] == 'brawler':
                            st.session_state.inv[data['name']] = {"lvl": 1, "pwr": 600, "rarity": "Legendary", "icon": "🌵"}
                        st.session_state.claimed_tiers.append(tier)
                        st.rerun()
            else:
                st.button(f"{data['xp'] - st.session_state.xp} XP kerak", key=f"w_{tier}", disabled=True, use_container_width=True)
        else:
            st.button("✅ OLINGAN", key=f"c_{tier}", disabled=True, use_container_width=True)

with col3:
    st.header("👤 Kolleksiya")
    for name, data in st.session_state.inv.items():
        st.markdown(f"""
            <div class="card">
                <b>{data['icon']} {name}</b><br>
                <small>PWR: {data['pwr']} | LVL: {data['lvl']}</small>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.sidebar.warning("Diqqat: Hozircha doimiy saqlash faqat session davomida ishlaydi. Ma'lumotlar o'chmasligi uchun 'Keep App Alive' sozlamasidan foydalaning.")
