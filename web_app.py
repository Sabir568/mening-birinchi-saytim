import streamlit as st
import random
import time

# --- SUPREME ENGINE CONFIG ---
st.set_page_config(page_title="Brawl Stars: GOD ENGINE", page_icon="⚡", layout="wide")

# --- ULTRA CSS INTERFACE ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #fff; font-family: 'Segoe UI', sans-serif; }
    
    /* Header & Stats */
    .header-bar {
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        padding: 20px; border-radius: 25px; border: 2px solid #00d2ff;
        text-align: center; margin-bottom: 25px;
    }
    .stat-val { color: #f1c40f; font-weight: bold; font-size: 24px; margin: 0 15px; }
    
    /* Advanced Box Styling */
    .box-container {
        border-radius: 30px; padding: 30px; text-align: center;
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(255,255,255,0.1); cursor: pointer;
    }
    .box-container:hover { transform: scale(1.05); border-color: #00d2ff; }
    .big-box { background: linear-gradient(135deg, #e91e63, #9c27b0); box-shadow: 0 10px 30px rgba(233,30,99,0.3); }
    .mega-box { background: linear-gradient(135deg, #2196f3, #00bcd4); box-shadow: 0 10px 30px rgba(33,150,243,0.3); }
    .omega-box { background: linear-gradient(135deg, #ff9800, #ff5722); box-shadow: 0 10px 30px rgba(255,152,0,0.3); }

    /* Brawler Card */
    .brawler-card {
        background: rgba(255,255,255,0.05); border-radius: 20px;
        padding: 15px; margin-bottom: 10px; border-left: 6px solid #00d2ff;
        display: flex; align-items: center; gap: 15px;
    }
    .legendary-border { border-left-color: #f1c40f; box-shadow: 0 0 10px rgba(241,196,15,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE & STATE ---
BRAWLERS_DATA = {
    "LEON": {"rarity": "Legendary", "icon": "🦎", "hp": 3200, "dmg": 440, "color": "#f1c40f"},
    "SPIKE": {"rarity": "Legendary", "icon": "🌵", "hp": 2400, "dmg": 560, "color": "#f1c40f"},
    "MORTIS": {"rarity": "Mythic", "icon": "🦇", "hp": 3800, "dmg": 900, "color": "#e91e63"},
    "EDGAR": {"rarity": "Epic", "icon": "🧣", "hp": 3000, "dmg": 540, "color": "#9c27b0"},
    "COLT": {"rarity": "Rare", "icon": "🔫", "hp": 2800, "dmg": 360, "color": "#2196f3"},
    "SURGE": {"rarity": "Chromatic", "icon": "🤖", "hp": 3300, "dmg": 480, "color": "#00bcd4"}
}

for key in ['gold', 'gems', 'trophies', 'inv', 'logs', 'pass_exp']:
    if key not in st.session_state:
        if key == 'gold': st.session_state[key] = 5000
        elif key == 'gems': st.session_state[key] = 200
        elif key == 'inv': st.session_state[key] = {"SHELLY": {"lvl": 1, "pwr": 300, "icon": "🔫"}}
        else: st.session_state[key] = 0 if key in ['trophies', 'pass_exp'] else []

# --- CORE FUNCTIONS ---
def open_box(b_type):
    with st.spinner("🌀 Quti ochilmoqda..."):
        time.sleep(1.5)
    
    prices = {"BIG": 500, "MEGA": 80, "OMEGA": 150}
    if b_type == "BIG": st.session_state.gold -= prices[b_type]
    else: st.session_state.gems -= prices[b_type]

    luck = random.random()
    chance = {"BIG": 0.2, "MEGA": 0.45, "OMEGA": 0.7}[b_type]

    if luck < chance:
        name = random.choice(list(BRAWLERS_DATA.keys()))
        if name not in st.session_state.inv:
            data = BRAWLERS_DATA[name]
            st.session_state.inv[name] = {"lvl": 1, "pwr": data['dmg'], "icon": data['icon']}
            st.session_state.logs.insert(0, f"🌟 YANGI JANGCHI: {name}!")
            st.balloons()
        else:
            st.session_state.gold += 1500
            st.session_state.logs.insert(0, f"💰 Dublikat {name}: +1500 Oltin")
    else:
        st.session_state.gold += random.randint(200, 800)
        st.session_state.pass_exp += 20
        st.session_state.logs.insert(0, "📦 Qutidan resurslar chiqdi")

def start_battle():
    # Realistik Arena Simulation
    player_power = sum(v['pwr'] for v in st.session_state.inv.values())
    enemy_power = random.randint(300, 1500 + st.session_state.trophies // 2)
    
    if player_power > enemy_power:
        win_t = random.randint(8, 12)
        st.session_state.trophies += win_t
        st.session_state.gold += 100
        st.session_state.pass_exp += 50
        st.success(f"G'ALABA! +{win_t} Kubok, +100 Oltin")
    else:
        loss_t = random.randint(4, 7)
        st.session_state.trophies = max(0, st.session_state.trophies - loss_t)
        st.error(f"MAG'LUBIYAT! -{loss_t} Kubok")

# --- UI LAYOUT ---
st.markdown(f"""
    <div class='header-bar'>
        <h1>🏆 BRAWL STARS: GOD ENGINE v12</h1>
        <span class='stat-val'>💰 {st.session_state.gold:,}</span>
        <span class='stat-val'>💎 {st.session_state.gems}</span>
        <span class='stat-val'>🏆 {st.session_state.trophies}</span>
    </div>
    """, unsafe_allow_html=True)

# Main Grid
col_shop, col_game, col_inv = st.columns([1, 1, 1])

with col_shop:
    st.subheader("🛍️ PREMIUM SHOP")
    
    st.markdown("<div class='box-container big-box'><h1>🎁</h1><h3>BIG BOX</h3></div>", unsafe_allow_html=True)
    if st.button("500 OLTIN", use_container_width=True):
        if st.session_state.gold >= 500: open_box("BIG"); st.rerun()
    
    st.markdown("<div class='box-container mega-box'><h1>🔵</h1><h3>MEGA BOX</h3></div>", unsafe_allow_html=True)
    if st.button("80 GEM", use_container_width=True):
        if st.session_state.gems >= 80: open_box("MEGA"); st.rerun()

    st.markdown("<div class='box-container omega-box'><h1>🟣</h1><h3>OMEGA BOX</h3></div>", unsafe_allow_html=True)
    if st.button("150 GEM", use_container_width=True):
        if st.session_state.gems >= 150: open_box("OMEGA"); st.rerun()

with col_game:
    st.subheader("⚔️ ARENA MODE")
    if st.button("🔥 JANGGA KIRISH (PLAY)", use_container_width=True):
        start_battle()
        st.rerun()
    
    st.write("---")
    st.subheader("🎫 BRAWL PASS")
    progress = (st.session_state.pass_exp % 500) / 500
    st.progress(progress)
    st.write(f"Level: {st.session_state.pass_exp // 500} | XP: {st.session_state.pass_exp % 500}/500")
    
    if st.button("🎁 MUKOFOTNI OLISH"):
        if st.session_state.pass_exp >= 500:
            st.session_state.gems += 50
            st.session_state.pass_exp -= 500
            st.toast("Brawl Pass Mukofoti: +50 Gem!")
            st.rerun()

with col_inv:
    st.subheader("👤 MY BRAWLERS")
    for name, data in st.session_state.inv.items():
        is_leg = "legendary-border" if name in BRAWLERS_DATA and BRAWLERS_DATA[name]['rarity'] == "Legendary" else ""
        st.markdown(f"""
            <div class='brawler-card {is_leg}'>
                <span style='font-size: 30px;'>{data['icon']}</span>
                <div>
                    <b>{name}</b><br>
                    <small>Level: {data['lvl']} | Power: {data['pwr']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        up_cost = data['lvl'] * 1000
        if st.button(f"UPGRADE ({up_cost} 💰)", key=f"up_{name}"):
            if st.session_state.gold >= up_cost:
                st.session_state.gold -= up_cost
                st.session_state.inv[name]['lvl'] += 1
                st.session_state.inv[name]['pwr'] += 100
                st.rerun()

# Logs at bottom
st.write("---")
st.subheader("📜 O'YIN JURNALI")
for log in st.session_state.logs[:5]:
    st.caption(log)

if st.sidebar.button("♻️ RESET ALL DATA"):
    st.session_state.clear()
    st.rerun()
