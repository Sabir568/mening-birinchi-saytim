import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars Elite", page_icon="🔱", layout="wide")

# --- 2. SUPREME CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .event-card { background: linear-gradient(135deg, #ff0055 0, #6200ff 100%); border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; box-shadow: 0 0 20px rgba(255,0,85,0.4); margin-bottom: 15px; }
    .pass-panel { background: rgba(10, 0, 30, 0.85); border: 2px solid #6200ff; border-radius: 20px; padding: 20px; height: 600px; overflow-y: scroll; }
    .tier-item { background: #0a0a0a; border-radius: 10px; padding: 10px; margin-bottom: 8px; border-left: 5px solid #6200ff; display: flex; justify-content: space-between; align-items: center; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 5px; }
    .rank-badge { background: #cd7f32; color: white; padding: 2px 5px; border-radius: 4px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"pwr": 300, "icon": "🔫", "rank": "BRONZE III"}},
        'claimed': [], 'plus': False
    })

BRAWLERS_DB = {
    "Леон": {"icon": "🦎", "rank": "SILVER I"},
    "Ворон": {"icon": "🦅", "rank": "BRONZE II"},
    "Спайк": {"icon": "🌵", "rank": "GOLD I"},
    "Мортис": {"icon": "🦇", "rank": "BRONZE III"},
    "Сэнди": {"icon": "⏳", "rank": "SILVER II"}
}

# --- 4. CORE LOGIC ---
def open_box(cost, chance, is_mega=False):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 ОТКРЫТИЕ..."):
            time.sleep(0.8)
            if random.random() < chance:
                new_b = random.choice([b for b in BRAWLERS_DB.keys() if b not in st.session_state.inv])
                if new_b:
                    st.session_state.inv[new_b] = BRAWLERS_DB[new_b]
                    st.balloons(); st.success(f"🔥 НОВЫЙ БОЕЦ: {new_b}!")
                else: # Agar hamma brawler bo'lsa
                    st.session_state.gold += (cost * 2)
                    st.info("💰 Все бойцы собраны! Золото возвращено.")
            else:
                if is_mega: # Mega Box uchun kompensatsiya
                    refund = 12000
                    st.session_state.gold += refund
                    st.info(f"🍀 Боец не выпал, но вы получили УЛЬТРА КЭШБЭК: {refund} 💰")
                else:
                    gain = random.randint(int(cost*0.5), int(cost*0.9))
                    st.session_state.gold += gain
                    st.toast(f"📦 +{gain} ЗОЛОТА")
    else:
        st.error(f"Недостаточно золота! Нужно {cost}")

# --- 5. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: REVOLUTION v19.2 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🛒 МАГАЗИН")
    st.markdown("<div class='event-card'><small>ОСТАЛОСЬ: 24 ЧАСА</small><h3>💎 МЕГА УЛЬТРА ЯЩИК</h3><p>10,000 💰</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ МЕГА ЯЩИК", use_container_width=True):
        open_box(10000, 0.5, is_mega=True); st.rerun()
    
    for c, n in [(500, "МАЛЫЙ"), (1000, "БОЛЬШОЙ"), (3000, "МЕГА")]:
        st.markdown(f"<div style='background:#111; padding:10px; border-radius:10px; margin-bottom:5px; text-align:center; border:1px solid #333;'>{n} ЯЩИК - {c} 💰</div>", unsafe_allow_html=True)
        if st.button(f"КУПИТЬ {n}", key=f"shop_{c}", use_container_width=True):
            open_box(c, 0.1); st.rerun()

with col2:
    st.header("⚔️ АРЕНА")
    if st.button("🔥 НАЧАТЬ БОЙ (+100 💰)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 400 # Progressni qiyinlashtirdik
        st.session_state.trophies += 10; st.rerun()
    
    st.write("---")
    st.subheader("💾 ДАННЫЕ")
    if st.button("СОХРАНИТЬ КОД"):
        data = {k: v for k, v in st.session_state.items() if k != 'save_code'}
        st.code(base64.b64encode(json.dumps(data).encode()).decode())
    
    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            for k, v in d.items(): st.session_state[k] = v
            st.success("Загружено!"); time.sleep(0.5); st.rerun()
        except: st.error("Ошибка!")

with col3:
    st.header("🎫 БРАВЛ ПАСС (30 LVL)")
    st.write(f"ОПЫТ (XP): {st.session_state.xp:,}")
    
    if not st.session_state.plus:
        if st.button("💎 КУПИТЬ ПЛЮС (200 ГЕМОВ)", use_container_width=True):
            if st.session_state.gems >= 200:
                st.session_state.gems -= 200; st.session_state.plus = True; st.rerun()
    else: st.success("БРАВЛ ПАСС ПЛЮС: АКТИВЕН ✅")

    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 31):
        req_xp = i * 2500 # Har bir lvl uchun 2500 XP kerak (Qiyin)
        is_plus_tier = i % 5 == 0
        claimed = i in st.session_state.claimed
        unlocked = st.session_state.xp >= req_xp
        
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        color = "#ff0055" if is_plus_tier else "#6200ff"
        
        st.markdown(f"""<div class='tier-item' style='border-left-color:{color}'>
            <span>Уровень {i} {'(PLUS)' if is_plus_tier else ''}</span>
            <span>{status}</span>
        </div>""", unsafe_allow_html=True)
        
        if unlocked and not claimed:
            if is_plus_tier and not st.session_state.plus:
                st.button("Нужен Плюс", key=f"l_{i}", disabled=True, use_container_width=True)
            else:
                if st.button(f"Забрать {i}", key=f"c_{i}", use_container_width=True):
                    if i == 30: st.session_state.gold += 400000
                    else: st.session_state.gold += 2000
                    st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header("👤 МОИ БОЙЦЫ")
cols = st.columns(4)
for i, (name, info) in enumerate(st.session_state.inv.items()):
    with cols[i % 4]:
        st.markdown(f"<div class='brawler-card'><span class='rank-badge'>{info.get('rank','BRONZE I')}</span><br><h2>{info.get('icon','👤')}</h2><b>{name}</b></div>", unsafe_allow_html=True)
