import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars Sirius", page_icon="🔱", layout="wide")

# --- 2. SUPREME CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .event-card { background: linear-gradient(135deg, #00d2ff 0, #3a7bd5 100%); border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; box-shadow: 0 0 20px rgba(0,210,255,0.4); margin-bottom: 15px; }
    .pass-panel { background: rgba(10, 0, 30, 0.85); border: 2px solid #6200ff; border-radius: 20px; padding: 20px; height: 550px; overflow-y: scroll; }
    .tier-item { background: #0a0a0a; border-radius: 10px; padding: 10px; margin-bottom: 8px; border-left: 5px solid #6200ff; display: flex; justify-content: space-between; align-items: center; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 5px; }
    .sirius-style { border: 2px solid #00d2ff !important; box-shadow: 0 0 15px #00d2ff; color: #00d2ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 100, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": "🔫"},
        'claimed': [], 'plus': False
    })

# --- 4. CORE FUNCTIONS ---
def open_mega_ultra():
    if st.session_state.gold >= 10000:
        st.session_state.gold -= 10000
        with st.spinner("📦 ОТКРЫТИЕ МЕГА УЛЬТРА..."):
            time.sleep(1)
            rand = random.random()
            
            # 20% Kristall tushishi
            if rand < 0.20:
                reward = random.randint(50, 150)
                st.session_state.gems += reward
                st.balloons()
                st.success(f"💎 НЕВЕРОЯТНО! Вы получили {reward} Гемов!")
            
            # 10% Sirius yoki yangi brawler
            elif rand < 0.30:
                available = ["SIRIUS", "Леон", "Ворон", "Спайк"]
                new_b = random.choice([b for b in available if b not in st.session_state.inv])
                if new_b:
                    st.session_state.inv[new_b] = "🌟" if new_b == "SIRIUS" else "🔥"
                    st.balloons()
                    st.success(f"🔥 НОВЫЙ БОЕЦ: {new_b}!")
                else:
                    st.session_state.gold += 15000
                    st.info("🍀 Все бойцы есть! Кэшбэк 15,000 💰")
            
            # Qolgan holatlarda oltin qaytishi
            else:
                st.session_state.gold += 12000
                st.info("🍀 Гемы не выпали, но вы получили Кэшбэк: 12,000 💰")
    else:
        st.error("Недостаточно золота!")

# --- 5. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: SIRIUS v20.1 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🛒 МАГАЗИН")
    st.markdown("<div class='event-card'><h3>💎 МЕГА УЛЬТРА ЯЩИК</h3><p>10,000 💰</p><small>ШАНС НА ГЕМЫ: 20%</small></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ МЕГА УЛЬТРА", use_container_width=True):
        open_mega_ultra(); st.rerun()
    
    st.write("---")
    if st.button("МАЛЫЙ ЯЩИК (500 💰)", use_container_width=True):
        if st.session_state.gold >= 500:
            st.session_state.gold -= 500
            if random.random() < 0.05:
                st.session_state.inv["Кольт"] = "🔫"
                st.success("Новый боец!")
            else: st.session_state.gold += 400; st.toast("+400 💰")
            st.rerun()

with col2:
    st.header("⚔️ АРЕНА")
    if st.button("🔥 В БОЙ! (+100 💰 | +150 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 150
        st.session_state.trophies += 10; st.rerun()
    
    st.write("---")
    st.subheader("💾 АККАУНТ")
    if st.button("СОЗДАТЬ КОД", use_container_width=True):
        data = {k: v for k, v in st.session_state.items()}
        st.code(base64.b64encode(json.dumps(data).encode()).decode())

    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ", use_container_width=True):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            for k, v in d.items(): st.session_state[k] = v
            st.success("Успешно!"); st.rerun()
        except: st.error("Ошибка!")

with col3:
    st.header("🎫 BRAWL PASS (30 LVL)")
    if not st.session_state.plus:
        if st.button("💎 КУПИТЬ ПЛЮС (200 ГЕМОВ)", use_container_width=True):
            if st.session_state.gems >= 200:
                st.session_state.gems -= 200; st.session_state.plus = True; st.rerun()
            else: st.error("Нужно 200 Гемов!")

    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 31):
        unlocked = st.session_state.xp >= i * 5000
        claimed = i in st.session_state.claimed
        is_plus = i % 5 == 0
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        
        st.markdown(f"<div class='tier-item'><span>Lvl {i} {'(PLUS)' if is_plus else ''}</span> <span>{status}</span></div>", unsafe_allow_html=True)
        if unlocked and not claimed:
            if is_plus and not st.session_state.plus:
                st.button("Нужен Плюс", key=f"l_{i}", disabled=True)
            elif st.button(f"Забрать {i}", key=f"c_{i}"):
                st.session_state.gold += 3000
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header("👤 МОИ БОЙЦЫ")
cols = st.columns(4)
for i, (name, icon) in enumerate(st.session_state.inv.items()):
    with cols[i % 4]:
        sirius_class = "sirius-style" if name == "SIRIUS" else ""
        st.markdown(f"<div class='brawler-card {sirius_class}'><h2>{icon}</h2><b>{name}</b></div>", unsafe_allow_html=True)
