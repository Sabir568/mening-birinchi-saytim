import streamlit as st
import random
import time

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars TITAN", page_icon="🔱", layout="wide")

# --- 2. TITAN VISUALS (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #050a10; color: #e0e0e0; }
    .header-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px; border-radius: 20px; border: 2px solid #f1c40f;
        text-align: center; box-shadow: 0 10px 30px rgba(241, 196, 15, 0.2);
    }
    .resource-card {
        background: rgba(0,0,0,0.5); border: 1px solid #333;
        border-radius: 15px; padding: 15px; text-align: center;
    }
    .pass-plus {
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        color: #000; border-radius: 15px; padding: 20px;
        font-weight: bold; margin-bottom: 20px; border: 3px solid #fff;
    }
    .b-card {
        background: #111; border: 1px solid #444; border-radius: 12px;
        padding: 10px; margin-bottom: 8px; border-left: 5px solid #00d2ff;
    }
    .legendary { border-left-color: #f1c40f; background: #1a1a00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SYSTEM STATE (0 DAN BOSHLANISHI) ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Shelly": {"lvl": 1, "pwr": 300, "rarity": "Common", "icon": "🔫"}},
        'claimed_tiers': [], 'plus_active': False
    })

BRAWLERS_DB = {
    "Leon": {"rarity": "Legendary", "pwr": 600, "icon": "🦎"},
    "Crow": {"rarity": "Legendary", "pwr": 580, "icon": "🦅"},
    "Spike": {"rarity": "Legendary", "pwr": 620, "icon": "🌵"},
    "Mortis": {"rarity": "Mythic", "pwr": 500, "icon": "🦇"},
    "Surge": {"rarity": "Chromatic", "pwr": 550, "icon": "🤖"}
}

# --- 4. BRAWL PASS PLUS TIZIMI (KO'PAYTIRILGAN DARAJALAR) ---
PASS_REWARDS = {
    1: {"xp": 1000, "reward": "500 Gold", "type": "gold", "val": 500},
    2: {"xp": 3000, "reward": "20 Gems", "type": "gems", "val": 20},
    3: {"xp": 7000, "reward": "1500 Gold", "type": "gold", "val": 1500},
    4: {"xp": 15000, "reward": "50 Gems", "type": "gems", "val": 50},
    5: {"xp": 30000, "reward": "Mega Box", "type": "box"},
    6: {"xp": 60000, "reward": "5000 Gold", "type": "gold", "val": 5000},
    7: {"xp": 120000, "reward": "Legendary Brawler", "type": "brawler"},
    8: {"xp": 250000, "reward": "10,000 Gold", "type": "gold", "val": 10000},
    9: {"xp": 500000, "reward": "PLUS FINAL: 400,000 GOLD", "type": "gold", "val": 400000}
}

# --- 5. LOGIC ---
def battle():
    time.sleep(1) # Jang vaqti
    win = random.choices([True, False], weights=[0.4, 0.6])[0] # Yutish qiyinroq
    if win:
        st.session_state.trophies += 8
        st.session_state.gold += 50
        st.session_state.xp += 400
        return True
    else:
        st.session_state.trophies = max(0, st.session_state.trophies - 6)
        st.session_state.xp += 100 # Mag'lubiyatda kam XP
        return False

# --- 6. INTERFACE ---
st.markdown(f"""
    <div class='header-box'>
        <h1>🔱 BRAWL STARS: TITAN EDITION v16 🔱</h1>
        <div style='display: flex; justify-content: space-around; margin-top: 15px;'>
            <span style='color: #f1c40f; font-size: 20px;'>💰 {st.session_state.gold:,}</span>
            <span style='color: #00d2ff; font-size: 20px;'>💎 {st.session_state.gems}</span>
            <span style='color: #ffffff; font-size: 20px;'>🏆 {st.session_state.trophies}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_game, col_pass, col_inv = st.columns([1, 1.5, 1])

# --- JANG VA DO'KON ---
with col_game:
    st.header("⚔️ Arena")
    if st.button("🔥 JANGGA KIRISH (PLAY)", use_container_width=True, type="primary"):
        res = battle()
        if res: st.success("G'alaba! +400 XP")
        else: st.error("Mag'lubiyat! +100 XP")
        st.rerun()

    st.write("---")
    st.subheader("🛒 Shop")
    if st.button("Big Box (500 💰)", use_container_width=True):
        if st.session_state.gold >= 500:
            st.session_state.gold -= 500
            if random.random() < 0.15:
                name = random.choice(list(BRAWLERS_DB.keys()))
                st.session_state.inv[name] = BRAWLERS_DB[name]
                st.balloons()
            else: st.toast("Faqat tangalar chiqdi...")
            st.rerun()

    if not st.session_state.plus_active:
        st.markdown("<div class='pass-plus'>BRAWL PASS PLUS<br><small>200 Gems kerak</small></div>", unsafe_allow_html=True)
        if st.button("PLUS SOTIB OLISH (200 💎)", use_container_width=True):
            if st.session_state.gems >= 200:
                st.session_state.gems -= 200
                st.session_state.plus_active = True
                st.rerun()

# --- BRAWL PASS PLUS ---
with col_pass:
    st.header("🎫 Brawl Pass Plus")
    st.write(f"Sizning XP: **{st.session_state.xp:,}**")
    
    for tier, data in PASS_REWARDS.items():
        is_plus_tier = tier > 5
        claimed = tier in st.session_state.claimed_tiers
        can_claim = st.session_state.xp >= data['xp']
        
        # Plus blokirovka
        if is_plus_tier and not st.session_state.plus_active:
            st.markdown(f"<div class='b-card' style='opacity: 0.5;'>🔒 Tier {tier}: {data['reward']} (Plus Kerak)</div>", unsafe_allow_html=True)
            continue

        col1, col2 = st.columns([3, 1])
        with col1:
            color = "gold" if is_plus_tier else "white"
            st.markdown(f"<div class='b-card' style='color: {color};'><b>Tier {tier}:</b> {data['reward']} <br><small>{data['xp']:,} XP</small></div>", unsafe_allow_html=True)
        with col2:
            if claimed:
                st.button("✅", key=f"cl_{tier}", disabled=True)
            elif can_claim:
                if st.button("OLISH", key=f"get_{tier}"):
                    if data['type'] == 'gold': st.session_state.gold += data['val']
                    elif data['type'] == 'gems': st.session_state.gems += data['val']
                    elif data['type'] == 'brawler':
                        st.session_state.inv["Spike"] = BRAWLERS_DB["Spike"]
                    st.session_state.claimed_tiers.append(tier)
                    st.rerun()
            else:
                st.button("🔒", key=f"lock_{tier}", disabled=True)

# --- KOLLEKSIYA ---
with col_inv:
    st.header("👤 Collection")
    for name, data in st.session_state.inv.items():
        is_leg = "legendary" if data.get('rarity') == "Legendary" else ""
        st.markdown(f"""
            <div class='b-card {is_leg}'>
                <span style='font-size: 25px;'>{data['icon']}</span> <b>{name}</b><br>
                <small>{data.get('rarity', 'Common')} | PWR: {data.get('pwr', 300)}</small>
            </div>
        """, unsafe_allow_html=True)

if st.sidebar.button("⚠️ RESET ALL (0 DAN BOSHLASH)"):
    st.session_state.clear()
    st.rerun()
