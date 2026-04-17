import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars FIXED", page_icon="💎", layout="wide")

# --- 2. SUPREME CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .gift-box { background: rgba(0, 255, 204, 0.1); border: 2px dashed #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .code-display { font-size: 30px; font-weight: bold; color: #ff0055; background: white; padding: 10px; border-radius: 10px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
# Sovg'a kodlarini saqlash uchun lug'at (Dictionary)
if 'active_gifts' not in st.session_state:
    st.session_state.active_gifts = {}

if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 100, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"icon": "🔫", "rank": "BRONZE III"}},
        'claimed': [], 'plus': False
    })

# --- 4. CORE FUNCTIONS ---
def open_box(cost, chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        if random.random() < chance:
            st.balloons()
            st.success("НОВЫЙ БОЕЦ!")
        else:
            st.session_state.gold += int(cost * 0.7)
            st.toast("Почти повезло!")
    else:
        st.error("Не хватает золота!")

# --- 5. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: STABLE v19.5 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🛒 МАГАЗИН")
    if st.button("ОТКРЫТЬ ЯЩИК (3000 💰)", use_container_width=True):
        open_box(3000, 0.2)
        st.rerun()

    st.write("---")
    # GIFT SECTION
    st.markdown("<div class='gift-box'>", unsafe_allow_html=True)
    st.subheader("🎁 ПОДАРОК")
    amount = st.number_input("Сколько Гемов:", min_value=1, max_value=max(1, st.session_state.gems), step=1)
    
    if st.button("СОЗДАТЬ КОД 🎫"):
        if st.session_state.gems >= amount:
            st.session_state.gems -= amount
            # Oddiy 4 xonali kod yaratish
            simple_code = str(random.randint(1000, 9999))
            st.session_state.active_gifts[simple_code] = amount
            st.session_state.last_code = simple_code # Kod yo'qolib ketmasligi uchun
            st.success(f"Списано {amount} 💎")
        else:
            st.error("Недостаточно Гемов!")

    # Kodni ko'rsatish (yo'qolib ketmaydi)
    if 'last_code' in st.session_state:
        st.markdown("Ваш код для друга:")
        st.markdown(f"<div class='code-display'>{st.session_state.last_code}</div>", unsafe_allow_html=True)
        st.info("Передайте этот номер другу!")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.header("⚔️ АРЕНА")
    if st.button("🔥 В БОЙ!", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 150
        st.rerun()

    st.write("---")
    st.subheader("📥 ПРИНЯТЬ ПОДАРОК")
    claim_code = st.text_input("Введите 4-значный код:", placeholder="Например: 3628")
    if st.button("ПОЛУЧИТЬ 💎", use_container_width=True):
        if claim_code in st.session_state.active_gifts:
            gift_val = st.session_state.active_gifts.pop(claim_code)
            st.session_state.gems += gift_val
            st.balloons()
            st.success(f"Ура! Вы получили {gift_val} Гемов!")
            if 'last_code' in st.session_state and st.session_state.last_code == claim_code:
                del st.session_state.last_code
            time.sleep(1)
            st.rerun()
        else:
            st.error("Код неверный или уже использован!")

with col3:
    st.header("🎫 BRAWL PASS")
    st.write(f"XP: {st.session_state.xp}/150,000")
    st.progress(min(st.session_state.xp/150000, 1.0))
    
    st.header("👤 БОЙЦЫ")
    for b in st.session_state.inv:
        st.markdown(f"<div style='background:#111; padding:10px; border-radius:10px; margin-bottom:5px;'>{b}</div>", unsafe_allow_html=True)
