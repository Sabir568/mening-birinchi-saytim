import streamlit as st
import random
import time
import base64
import json

# --- 1. GLOBAL STYLING ---
st.set_page_config(page_title="RECKAT GRAND UPDATE", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700&display=swap');
    .stApp { background: #050505; color: #ffffff; font-family: 'Inter', sans-serif; }
    .luxury-card { background: #111; border: 1px solid #222; border-radius: 15px; overflow: hidden; margin-bottom: 25px; transition: 0.3s; }
    .luxury-card:hover { border-color: #00ffcc; }
    .price-tag { color: #00ffcc; font-weight: bold; font-size: 18px; padding: 5px 15px; }
    .container-box { background: linear-gradient(45deg, #1a1a1a, #333); border: 2px solid #6200ff; padding: 20px; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE & ASSETS ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'used_promos': [],
        'inventory': []
    })

# Market Prices for Selling (Budgeting)
PRICES = {
    "Porsche 911": 1250000,
    "Bugatti Chiron": 7500000,
    "BMW M3 G80": 70000,
    "Bel Air Mansion, LA": 1500000,
    "Beverly Hills Villa": 3000000,
    "Malibu Oceanfront": 5000000,
    "McLaren 720S": 250000,
    "Rolls-Royce Cullinan": 400000
}

def get_save_code():
    data = {"g": st.session_state.gold, "m": st.session_state.gems, "x": st.session_state.xp, "up": st.session_state.used_promos, "inv": st.session_state.inventory}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save_code(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'used_promos':d['up'], 'inventory':d['inv']})
        return True
    except: return False

# --- 3. UI ---
st.title("🔱 RECKAT LUXURY & CONTAINERS")

# Dashboard
c1, c2, c3 = st.columns(3)
with c1: st.metric("CASH", f"${st.session_state.gold:,}")
with c2: st.metric("CRYSTALS", f"💎 {st.session_state.gems:,}")
with c3: st.metric("XP", f"⭐ {st.session_state.xp:,}")

st.write("---")

tab1, tab2, tab3, tab4 = st.tabs(["📦 CONTAINERS", "🏎️ SHOWROOM", "💼 INVENTORY & SELL", "⚙️ SYSTEM"])

with tab1:
    st.subheader("Exclusive Lootboxes")
    con1, con2 = st.columns(2)
    
    with con1:
        st.markdown("<div class='container-box'><h3>STANDARD CONTAINER</h3><h2>$850,000</h2></div>", unsafe_allow_html=True)
        if st.button("OPEN STANDARD BOX", use_container_width=True):
            if st.session_state.gold >= 850000:
                st.session_state.gold -= 850000
                res = random.random()
                if res <= 0.30:
                    st.session_state.gold += 400000
                    st.success("You found $400,000 Cash!")
                elif res <= 0.70:
                    st.session_state.gems += 250
                    st.success("You found 250 Crystals!")
                else:
                    st.session_state.inventory.append("Porsche 911")
                    st.balloons(); st.success("JACKPOT! Porsche 911 Unlocked!")
                st.rerun()
            else: st.error("Not enough money!")

    with con2:
        st.markdown("<div class='container-box'><h3>ULTRA CONTAINER</h3><h2>$3,500,000</h2></div>", unsafe_allow_html=True)
        if st.button("OPEN ULTRA BOX", use_container_width=True):
            if st.session_state.gold >= 3500000:
                st.session_state.gold -= 3500000
                res = random.random()
                if res <= 0.60:
                    st.session_state.gold += 1250000
                    st.success("You found $1,250,000 Cash!")
                elif res <= 0.80:
                    st.session_state.gems += 500
                    st.success("You found 500 Crystals!")
                elif res <= 0.90:
                    st.session_state.inventory.append("Bugatti Chiron")
                    st.balloons(); st.success("LEGENDARY! Bugatti Chiron Unlocked!")
                else:
                    st.info("The container was unstable. You received 1000 XP.")
                    st.session_state.xp += 1000
                st.rerun()
            else: st.error("Not enough money!")

with tab2:
    st.subheader("Luxury Cars")
    # Lamborghini rasm yangilandi
    st.markdown("""
    <div class='luxury-card'>
        <img src='https://images.unsplash.com/photo-1544636331-e26879cd4d9b?q=80&w=1000&auto=format&fit=crop' style='width:100%; height:400px; object-fit:cover;'>
        <div style='padding:15px;'><h3>Lamborghini Aventador SVJ</h3><p class='price-tag'>$650,000</p></div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("BUY LAMBORGHINI"):
        if st.session_state.gold >= 650000:
            st.session_state.gold -= 650000
            st.session_state.inventory.append("Lamborghini Aventador")
            st.success("Purchased!")
        else: st.error("No money!")

    st.write("---")
    st.subheader("New Brands")
    b1, b2 = st.columns(2)
    with b1:
        st.image("https://images.unsplash.com/photo-1621135802920-133df287f89c?q=80&w=1000&auto=format&fit=crop", caption="McLaren 720S - $350,000")
        if st.button("Buy McLaren"):
            if st.session_state.gold >= 350000: st.session_state.gold -= 350000; st.session_state.inventory.append("McLaren 720S"); st.rerun()
    with b2:
        st.image("https://images.unsplash.com/photo-1638319574109-7756f70a2731?q=80&w=1000&auto=format&fit=crop", caption="Rolls-Royce Cullinan - $450,000")
        if st.button("Buy Rolls-Royce"):
            if st.session_state.gold >= 450000: st.session_state.gold -= 450000; st.session_state.inventory.append("Rolls-Royce Cullinan"); st.rerun()

with tab3:
    st.subheader("Manage Your Assets")
    if not st.session_state.inventory:
        st.info("No assets to show.")
    else:
        for item in st.session_state.inventory:
            col_i, col_s = st.columns([3, 1])
            col_i.write(f"🏢 {item}")
            sell_price = PRICES.get(item, 50000)
            if col_s.button(f"SELL (${sell_price:,})", key=f"sell_{item}_{random.random()}"):
                st.session_state.gold += sell_price
                st.session_state.inventory.remove(item)
                st.success(f"Sold {item}!")
                st.rerun()

with tab4:
    st.subheader("Terminal")
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("GENERATE SAVE CODE"): st.code(get_save_code())
        l_code = st.text_input("LOAD CODE:")
        if st.button("RESTORE"):
            if load_save_code(l_code): st.success("Restored!"); st.rerun()
    with sc2:
        promo = st.text_input("PROMO CODE:").strip()
        if st.button("ACTIVATE"):
            # Yangi promo qo'shildi
            if promo == "newupdatew22" and "newupdatew22" not in st.session_state.used_promos:
                st.session_state.gold += 100000; st.session_state.gems += 50
                st.session_state.used_promos.append("newupdatew22"); st.balloons()
            # Avvalgi promolar saqlab qolindi
            elif promo == "REKCATv22" and "REKCATv22" not in st.session_state.used_promos:
                st.session_state.gold += 250; st.session_state.gems += 30; st.session_state.used_promos.append("REKCATv22")
            elif promo == "KHIVA90":
                st.session_state.gold += 9000; st.session_state.gems += 90
            else: st.error("Invalid or already used.")
            st.rerun()

st.write("---")
if st.button("💰 QUICK EARN ($50,000)"):
    st.session_state.gold += 50000; st.rerun()
