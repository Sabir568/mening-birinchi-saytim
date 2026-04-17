import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars Promo", page_icon="🎫", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'sans-serif'; }
    .status-bar { background: rgba(0,210,255,0.1); border: 2px solid #00ffcc; border-radius: 20px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; }
    .sirius-glow { border: 2px solid #00d2ff !important; box-shadow: 0 0 15px #00d2ff; }
    .admin-glow { border: 2px solid gold !important; box-shadow: 0 0 15px gold; color: gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 100, 'xp': 0,
        'inv': {"Шелли": "🔫"},
        'plus': False
    })

# --- 4. PROMO CODES LOGIC ---
PROMOS = {
    "ADMIN777": {"gold": 1000000, "gems": 50000, "brawler": "ADMIN", "icon": "👑"},
    "SIRIUS2026": {"gold": 50000, "gems": 1000, "brawler": "SIRIUS", "icon": "🌟"},
    "FREEGEMS": {"gold": 0, "gems": 500, "brawler": None, "icon": None}
}

# --- 5. UI ---
st.title("🔱 BRAWL STARS: PROMO VERSION")

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span>💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span>💎 ГЕМЫ: {st.session_state.gems:,}</span>
    <span>⭐ XP: {st.session_state.xp}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.2])

with c1:
    st.header("🎫 ПРОМОКОД")
    promo_input = st.text_input("Введите промокод:", placeholder="Например: ADMIN777")
    if st.button("АКТИВИРОВАТЬ"):
        if promo_input in PROMOS:
            p = PROMOS[promo_input]
            st.session_state.gold += p["gold"]
            st.session_state.gems += p["gems"]
            if p["brawler"]:
                st.session_state.inv[p["brawler"]] = p["icon"]
            st.balloons()
            st.success(f"Промокод {promo_input} активирован!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Неверный промокод!")

    st.write("---")
    st.header("🛒 МАГАЗИН")
    if st.button("💎 МЕГА УЛЬТРА (10k)"):
        if st.session_state.gold >= 10000:
            st.session_state.gold -= 10000
            rand = random.random()
            if rand < 0.20: st.session_state.gems += 100; st.balloons()
            elif rand < 0.40: st.session_state.inv["ЛЕОН"] = "🦎"; st.balloons()
            else: st.session_state.gold += 12000
            st.rerun()

with c2:
    st.header("⚔️ АРЕНА")
    if st.button("🔥 В БОЙ!", use_container_width=True):
        st.session_state.gold += 100
        st.session_state.xp += 150; st.rerun()
    
    st.write("---")
    st.info("💡 Используйте промокоды для восстановления ресурсов после перезагрузки страницы.")

with c3:
    st.header("👤 МОИ БОЙЦЫ")
    cols = st.columns(2)
    for i, (name, icon) in enumerate(st.session_state.inv.items()):
        with cols[i % 2]:
            style = "admin-glow" if name == "ADMIN" else ("sirius-glow" if name == "SIRIUS" else "")
            st.markdown(f"<div class='brawler-card {style}'><h2>{icon}</h2><b>{name}</b></div>", unsafe_allow_html=True)
