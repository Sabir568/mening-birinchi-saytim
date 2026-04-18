import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIG & STYLES ---
st.set_page_config(page_title="RECKAT STARS v22", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #020202; color: #eee; font-family: 'Orbitron', sans-serif; }
    .main-title { font-family: 'Black Ops One', cursive; font-size: 60px; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #6200ff; }
    .status-bar { background: rgba(0,0,0,0.8); border: 2px solid #00ffcc; border-radius: 15px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; box-shadow: 0 0 15px #00ffcc; }
    .battle-box { background: #111; border: 3px solid #ff0055; border-radius: 20px; padding: 25px; text-align: center; box-shadow: inset 0 0 30px #ff0055; }
    .transfer-card { background: linear-gradient(135deg, #1a1a1a, #000); border: 1px solid #6200ff; border-radius: 15px; padding: 15px; margin-top: 10px; }
    .pass-area { background: #050505; border: 1px solid #444; height: 500px; overflow-y: scroll; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA & SESSION ---
BRAWLERS = ["Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"]

if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free',
        'used_promos': [], 'battle': False, 'ehp': 0
    })

# --- 3. SAVE/LOAD ENGINE (TEGILMADI) ---
def get_save():
    data = {"g":st.session_state.gold, "m":st.session_state.gems, "x":st.session_state.xp, "t":st.session_state.trophies, "i":st.session_state.inv, "c":st.session_state.claimed, "p":st.session_state.pass_type, "up": st.session_state.used_promos}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'trophies':d['t'], 'inv':d['i'], 'claimed':d['c'], 'pass_type':d['p'], 'used_promos': d.get('up', [])})
        return True
    except: return False

# --- 4. TRANSFER SYSTEM ---
def generate_transfer_code(amount, type_res):
    t_data = {"a": amount, "t": type_res, "salt": random.random()}
    return base64.b64encode(json.dumps(t_data).encode()).decode()[:4].upper()

# --- 5. UI ---
st.markdown("<div class='main-title'>RECKAT STARS v22</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="status-bar">
    <div style="color:#f1c40f">💰 {st.session_state.gold:,}</div>
    <div style="color:#00ffcc">💎 {st.session_state.gems:,}</div>
    <div style="color:#ffffff">🏆 {st.session_state.trophies:,}</div>
    <div style="color:#6200ff">⭐ {st.session_state.xp:,}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.6, 1, 1.4])

with col1:
    st.header("⚔️ АРЕНА БИТВЫ")
    if not st.session_state.battle:
        if st.button("🔥 ИГРАТЬ (В БОЙ)", use_container_width=True, type="primary"):
            st.session_state.battle = True
            st.session_state.ehp = random.randint(20, 50)
            st.rerun()
    else:
        st.markdown("<div class='battle-box'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size:100px;'>👾</h1>", unsafe_allow_html=True)
        st.write(f"HP ВРАГА: {st.session_state.ehp}")
        st.progress(max(st.session_state.ehp / 50, 0.0))
        if st.button("💥 УДАР!", use_container_width=True):
            st.session_state.ehp -= random.randint(2, 6)
            if st.session_state.ehp <= 0:
                st.session_state.battle = False
                g, x = random.randint(300, 600), 500
                st.session_state.gold += g; st.session_state.xp += x; st.session_state.trophies += 20
                st.balloons(); st.success(f"ПОБЕДА! +{g} 💰")
                time.sleep(1)
            st.rerun()
        if st.button("🏃 СБЕЖАТЬ", use_container_width=True):
            st.session_state.battle = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.header("🔄 ТРАНСФЕР (ПОДАРКИ)")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.subheader("Отправить")
        t_amt = st.number_input("Сколько:", min_value=1, step=10)
        t_type = st.selectbox("Что:", ["Золото", "Кристаллы"])
        if st.button("Создать 4-значный код"):
            if (t_type == "Золото" and st.session_state.gold >= t_amt) or (t_type == "Кристаллы" and st.session_state.gems >= t_amt):
                if t_type == "Золото": st.session_state.gold -= t_amt
                else: st.session_state.gems -= t_amt
                code = generate_transfer_code(t_amt, t_type)
                st.success(f"Код: {code}")
                st.info("Передайте этот код другу!")
            else: st.error("Недостаточно ресурсов!")
    with t_col2:
        st.subheader("Принять")
        get_code = st.text_input("Введите 4-значный код:").upper()
        if st.button("Получить"):
            st.warning("В этой демо-версии введите код, который создали выше.")
            # Haqiqiy sistemada bu bazaga ulanadi, hozircha simulyatsiya

with col2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("📝 СОЗДАТЬ SAVE", use_container_width=True): st.code(get_save())
    ld = st.text_input("ВСТАВИТЬ SAVE:")
    if st.button("📥 ЗАГРУЗИТЬ"):
        if load_save(ld): st.success("ОК!"); st.rerun()
    
    st.write("---")
    st.header("🔑 ПРОМОКОДЫ")
    pr = st.text_input("Код:").strip()
    if st.button("OK"):
        if pr == "REKCATv22" and "REKCATv22" not in st.session_state.used_promos:
            st.session_state.gold += 250; st.session_state.gems += 30
            st.session_state.used_promos.append("REKCATv22"); st.balloons()
        elif pr == "KHIVA90":
            st.session_state.gold += 9000; st.session_state.gems += 90; st.balloons()
        st.rerun()

with col3:
    st.header("🎫 RECKAT PASS")
    lvl = st.session_state.xp // 15000
    if st.session_state.pass_type == 'Free':
        if st.button("💎 PLUS (499 💎)"):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
    
    st.markdown("<div class='pass-area'>", unsafe_allow_html=True)
    for i in range(1, 51):
        is_ok = lvl >= i
        is_got = i in st.session_state.claimed
        c_p1, c_p2 = st.columns([2,1])
        c_p1.write(f"LVL {i}: {'✅' if is_got else ('🎁' if is_ok else '🔒')}")
        if is_ok and not is_got:
            if c_p2.button("GET", key=f"lv_{i}"):
                st.session_state.gold += 500; st.session_state.gems += 2
                if st.session_state.pass_type == 'Plus':
                    st.session_state.gold += 3000; st.session_state.gems += 20
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header(f"👥 КОЛЛЕКЦИЯ ({len(st.session_state.inv)}/78)")
ic = st.columns(6)
for idx, b in enumerate(st.session_state.inv):
    with ic[idx % 6]: st.markdown(f"<div style='background:#000; border:1px solid #00ffcc; padding:10px; border-radius:10px; text-align:center;'>{b}</div>", unsafe_allow_html=True)
