import streamlit as st
import random
import time
import base64
import json

# --- 1. KONFIGURATSIYA ---
st.set_page_config(page_title="RECKAT STARS", page_icon="🔱", layout="wide")

# --- 2. RECKAT STARS DIZAYNI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #050505 0%, #1a0033 100%); color: #ffffff; font-family: 'Orbitron', sans-serif; }
    .main-title { font-family: 'Black Ops One', cursive; font-size: 65px; text-align: center; color: #00ffcc; text-shadow: 4px 4px #6200ff; margin-bottom: 5px; }
    .status-bar { background: rgba(0, 0, 0, 0.9); border: 2px solid #6200ff; border-radius: 25px; padding: 20px; display: flex; justify-content: space-around; margin-bottom: 25px; box-shadow: 0 0 15px #6200ff; font-weight: bold; }
    .mega-ultra-box { background: linear-gradient(45deg, #6200ff, #ff00ff); border: 3px solid #00ffcc; box-shadow: 0 0 25px #00ffcc; text-align: center; padding: 20px; border-radius: 20px; margin-bottom: 15px; }
    .reckat-card { background: #000; border: 1px solid #444; border-radius: 12px; padding: 10px; text-align: center; margin-bottom: 8px; font-size: 14px; }
    .pass-scroll { background: rgba(10, 0, 20, 0.8); border-radius: 20px; padding: 15px; height: 600px; overflow-y: scroll; border: 2px solid #00ffcc; }
    .level-item { background: #1a1a1a; border-radius: 10px; padding: 12px; margin-bottom: 8px; border-left: 5px solid #00ffcc; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLERLAR RO'YXATI ---
ALL_BRAWLERS = [
    "Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", 
    "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", 
    "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", 
    "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", 
    "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", 
    "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"
]

# --- 4. BOSHLANG'ICH HOLAT (HAMMASI 0) ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free'
    })

# --- 5. LOGIKA VA SAVE/LOAD (TEGILMADI) ---
def get_save_code():
    data = {"g": st.session_state.gold, "m": st.session_state.gems, "x": st.session_state.xp, 
            "t": st.session_state.trophies, "i": st.session_state.inv, "c": st.session_state.claimed, "p": st.session_state.pass_type}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save_code(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'trophies':d['t'], 'inv':d['i'], 'claimed':d['c'], 'pass_type':d['p']})
        return True
    except: return False

def open_reckat_box(cost, chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        if random.random() < chance:
            possible = [b for b in ALL_BRAWLERS if b not in st.session_state.inv]
            if possible:
                new_b = random.choice(possible)
                st.session_state.inv.append(new_b)
                st.balloons(); st.success(f"🔥 НОВЫЙ БОЕЦ: {new_b}!")
        else:
            st.session_state.gold += int(cost * 0.4); st.toast("💨 Пусто! Кэшбэк 40%")
    else: st.error("Недостаточно золота!")

# --- 6. ASOSIY INTERFEYS ---
st.markdown("<div class='main-title'>RECKAT STARS</div>", unsafe_allow_html=True)

# Status paneli
st.markdown(f"""
<div class="status-bar">
    <div style="text-align:center; color:#f1c40f">💰 ЗОЛОТО<br>{st.session_state.gold:,}</div>
    <div style="text-align:center; color:#00ffcc">💎 КРИСТАЛЛЫ<br>{st.session_state.gems:,}</div>
    <div style="text-align:center; color:#ffffff">🏆 КУБКИ<br>{st.session_state.trophies:,}</div>
    <div style="text-align:center; color:#6200ff">⭐ ОПЫТ (XP)<br>{st.session_state.xp:,}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.2, 1, 1.3])

with c1:
    st.header("🏪 МАГАЗИН")
    st.markdown("<div class='mega-ultra-box'><h3>MEGA ULTRA BOX</h3><h2>10,000 💰</h2><p>Шанс: 25% | ⏳ 24 ЧАСА</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ MEGA ULTRA", use_container_width=True): open_reckat_box(10000, 0.25); st.rerun()
    
    st.write("---")
    if st.button("РЕККАТ ЯЩИК (5,000 💰)", use_container_width=True): open_reckat_box(5000, 0.15); st.rerun()
    
    st.header("⚔️ БИТВА")
    if st.button("🔥 В БОЙ (+100 💰 | +200 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 200
        st.session_state.trophies += 10; st.rerun()

with c2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("СОЗДАТЬ КОД", use_container_width=True): st.code(get_save_code())
    
    load_in = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ", use_container_width=True):
        if load_save_code(load_in): st.success("Загружено!"); st.rerun()
        else: st.error("Ошибка!")
    
    st.write("---")
    st.header("🎫 ПРОМОКОДЫ")
    promo = st.text_input("Введите код:").strip()
    if st.button("АКТИВИРОВАТЬ"):
        if promo == "APRIL2026" and "Сириус" not in st.session_state.inv:
            st.session_state.inv.append("Сириус"); st.balloons(); st.success("🌟 SIRIUS ВАШ!")
        elif promo == "KHIVA90":
            st.session_state.gold += 9000
            st.session_state.gems += 90
            st.balloons(); st.success("🎁 БОНУС: 9,000 ЗОЛОТА И 90 КРИСТАЛЛОВ!")
        else: st.error("Неверный код.")
        st.rerun()

with c3:
    st.header("🎫 RECKAT PASS PLUS")
    curr_lvl = st.session_state.xp // 15000
    st.write(f"Уровень: **{curr_lvl} / 50**")
    st.progress(min(curr_lvl/50, 1.0))
    
    if st.session_state.pass_type == 'Free':
        if st.button("💎 КУПИТЬ PLUS (499 💎)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
            else: st.error("Недостаточно кристаллов!")
    else: st.success("👑 PLUS АКТИВИРОВАН")

    st.markdown("<div class='pass-scroll'>", unsafe_allow_html=True)
    for i in range(1, 51):
        unlocked = curr_lvl >= i
        claimed = i in st.session_state.claimed
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        
        st.markdown(f"<div class='level-item'><span>УРОВЕНЬ {i}</span><span>{status}</span></div>", unsafe_allow_html=True)
        if unlocked and not claimed:
            if st.button(f"ЗАБРАТЬ {i}", key=f"lv_{i}"):
                st.session_state.gold += 500
                st.session_state.gems += 2 # Kristal yig'ish endi juda qiyin
                if st.session_state.pass_type == 'Plus':
                    st.session_state.gold += 2500
                    st.session_state.gems += 15 # Plus egalariga ko'proq
                    if i % 10 == 0:
                        new_r = random.choice([b for b in ALL_BRAWLERS if b not in st.session_state.inv])
                        if new_r: st.session_state.inv.append(new_r)
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header(f"👥 МОЯ КОЛЛЕКЦИЯ ({len(st.session_state.inv)}/78)")
cols = st.columns(6)
for idx, b in enumerate(st.session_state.inv):
    with cols[idx % 6]: st.markdown(f"<div class='reckat-card'>{b}</div>", unsafe_allow_html=True)
