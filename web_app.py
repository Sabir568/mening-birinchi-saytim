import streamlit as st
import random
import time
import base64
import json

# --- 1. GLOBAL STYLING ---
st.set_page_config(page_title="RECKAT STARS: ECONOMY", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Syncopate:wght@700&display=swap');
    .stApp { background: #000205; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .main-header { font-family: 'Syncopate', sans-serif; font-size: 55px; text-align: center; color: #00ffcc; text-shadow: 0 0 30px #00ffcc; padding: 20px; border-bottom: 2px solid #00ffcc; }
    .market-card { background: rgba(255, 217, 0, 0.05); border: 2px solid #f1c40f; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; transition: 0.3s; }
    .market-card:hover { transform: translateY(-5px); box-shadow: 0 0 20px #f1c40f; }
    .stat-box { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 10px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'level': 1,
        'modules': ["Engine v1"], 'claimed_milestones': [],
        'used_promos': [], 'in_warp': False, 'target_hp': 0,
        'unlocked_promos': [] # Sotib olingan promolar
    })

def get_save():
    data = {
        "g": st.session_state.gold, "m": st.session_state.gems, "x": st.session_state.xp,
        "l": st.session_state.level, "mod": st.session_state.modules, "cl": st.session_state.claimed_milestones,
        "up": st.session_state.used_promos, "un": st.session_state.unlocked_promos
    }
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({
            'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'level':d.get('l', 1),
            'modules':d['mod'], 'claimed_milestones':d['cl'], 'used_promos':d.get('up', []),
            'unlocked_promos': d.get('un', [])
        })
        return True
    except: return False

# --- 3. UI ---
st.markdown("<div class='main-header'>RECKAT STARS: MARKET</div>", unsafe_allow_html=True)

# Dashboard
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-box'>💰 КРЕДИТЫ<br>{st.session_state.gold:,}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'>💎 КРИСТАЛЛЫ<br>{st.session_state.gems:,}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-box'>⭐ XP<br>{st.session_state.xp:,}</div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-box'>📦 МОДУЛИ<br>{len(st.session_state.modules)}</div>", unsafe_allow_html=True)

st.write("---")

tab1, tab2, tab3 = st.tabs(["🛒 ЧЕРНЫЙ РЫНОК", "🌌 БИТВА", "🖥️ ТЕРМИНАЛ"])

with tab1:
    st.header("🏪 RECKAT BLACK MARKET")
    st.write("Здесь вы можете потратить свои Кредиты на эксклюзивные вещи.")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown("<div class='market-card'><h3>GEM BUNDLE</h3><p>Цена: 15,000 💰</p><p>Дает: Промокод на 50 💎</p></div>", unsafe_allow_html=True)
        if st.button("КУПИТЬ GEM BUNDLE"):
            if st.session_state.gold >= 15000:
                st.session_state.gold -= 15000
                code = f"GEM-{random.randint(100,999)}"
                st.session_state.unlocked_promos.append(code)
                st.success(f"Куплено! Ваш код: {code}")
            else: st.error("Недостаточно кредитов!")

    with m_col2:
        st.markdown("<div class='market-card'><h3>XP BOOST</h3><p>Цена: 8,000 💰</p><p>Дает: Промокод на 5,000 XP</p></div>", unsafe_allow_html=True)
        if st.button("КУПИТЬ XP BOOST"):
            if st.session_state.gold >= 8000:
                st.session_state.gold -= 8000
                code = f"XP-{random.randint(100,999)}"
                st.session_state.unlocked_promos.append(code)
                st.success(f"Куплено! Ваш код: {code}")
            else: st.error("Недостаточно кредитов!")

    with m_col3:
        st.markdown("<div class='market-card'><h3>SIRIUS TECH</h3><p>Цена: 50,000 💰</p><p>Дает: Модуль 'SIRIUS CORE'</p></div>", unsafe_allow_html=True)
        if st.button("КУПИТЬ SIRIUS TECH"):
            if st.session_state.gold >= 50000:
                st.session_state.gold -= 50000
                st.session_state.modules.append("SIRIUS CORE")
                st.balloons(); st.success("Технология SIRIUS добавлена в арсенал!")
            else: st.error("Недостаточно кредитов!")

with tab2:
    st.header("🌌 КОСМИЧЕСКАЯ АРЕНА")
    if not st.session_state.in_warp:
        if st.button("🚀 НАЧАТЬ ЗАЧИСТКУ СЕКТОРА", use_container_width=True):
            st.session_state.in_warp = True
            st.session_state.target_hp = random.randint(40, 80)
            st.rerun()
    else:
        st.write(f"### СТАТУС ВРАГА: {st.session_state.target_hp}%")
        st.progress(st.session_state.target_hp / 100)
        if st.button("📡 ОГОНЬ!"):
            st.session_state.target_hp -= random.randint(10, 20)
            if st.session_state.target_hp <= 0:
                st.session_state.in_warp = False
                win = random.randint(1000, 3000)
                st.session_state.gold += win
                st.session_state.xp += 800
                st.success(f"Сектор очищен! +{win} 💰"); st.balloons()
            st.rerun()

with tab3:
    st.header("🖥️ СИСТЕМНЫЙ ТЕРМИНАЛ")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.subheader("Активация кода")
        p_input = st.text_input("Введите код (купленный или секретный):").strip()
        if st.button("ВВОД"):
            if p_input.startswith("GEM-") and p_input in st.session_state.unlocked_promos:
                st.session_state.gems += 50
                st.session_state.unlocked_promos.remove(p_input)
                st.success("Активировано: +50 💎")
            elif p_input.startswith("XP-") and p_input in st.session_state.unlocked_promos:
                st.session_state.xp += 5000
                st.session_state.unlocked_promos.remove(p_input)
                st.success("Активировано: +5,000 XP")
            elif p_input == "REKCATv22" and "REKCATv22" not in st.session_state.used_promos:
                st.session_state.gold += 250; st.session_state.gems += 30; st.session_state.used_promos.append("REKCATv22")
                st.success("Бонус v22 получен!")
            elif p_input == "KHIVA90":
                st.session_state.gold += 9000; st.session_state.gems += 90; st.success("Привет из Хивы!")
            else: st.error("Неверный код или уже использован.")
            st.rerun()
            
    with t_col2:
        st.subheader("Backup & Save")
        if st.button("📝 СОЗДАТЬ КОД СОХРАНЕНИЯ"): st.code(get_save())
        l_input = st.text_input("Загрузить код:")
        if st.button("📥 ЗАГРУЗИТЬ"):
            if load_save(l_input): st.success("Данные загружены!"); st.rerun()

st.write("---")
st.header(f"📦 ВАШИ МОДУЛИ ({len(st.session_state.modules)})")
m_cols = st.columns(5)
for idx, mod in enumerate(st.session_state.modules):
    with m_cols[idx % 5]: st.info(mod)
