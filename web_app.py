import streamlit as st
import time

# Конфигурация страницы
st.set_page_config(page_title="Симулятор Миллионера 3.1", page_icon="💎", layout="wide")

# --- СУПЕР ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    .money-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    .money-text {
        font-size: 65px;
        font-weight: bold;
        color: #00ffcc;
    }
    .shop-item {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    .item-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 2px solid #333;
    }
    .inv-box {
        background: rgba(0, 255, 204, 0.1);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        border-left: 5px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ИГРЫ ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click' not in st.session_state: st.session_state.click = 150
if 'income' not in st.session_state: st.session_state.income = 0
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'last_tick' not in st.session_state: st.session_state.last_tick = time.time()

# Пассивный доход
now = time.time()
diff = int(now - st.session_state.last_tick)
if diff >= 1:
    st.session_state.money += diff * st.session_state.income
    st.session_state.last_tick = now

# --- ВЕРХНЯЯ ЧАСТЬ ---
st.markdown(f"""
    <div class='money-card'>
        <div style='font-size: 20px; color: #aaa;'>Ваш Баланс</div>
        <div class='money-text'>{st.session_state.money:,.0f} $</div>
    </div>
    """, unsafe_allow_html=True)

col_work, col_shop = st.columns([1, 2.5])

with col_work:
    st.header("💼 Карьера")
    if st.button("РАБОТАТЬ 👷‍♂️", use_container_width=True):
        st.session_state.money += st.session_state.click
        st.rerun()
    
    st.write(f"Доход за клик: **{st.session_state.click} $**")
    st.write(f"Доход в секунду: **{st.session_state.income} $**")
    
    st.write("---")
    st.header("🏠 Моё Имущество")
    if not st.session_state.inventory:
        st.write("У вас пока ничего нет.")
    else:
        for item in st.session_state.inventory:
            st.markdown(f"<div class='inv-box'>✅ {item}</div>", unsafe_allow_html=True)

with col_shop:
    st.header("🏪 Элитный Маркет")
    
    # Список товаров (С новыми ссылками)
    items = [
        {"name": "Chevrolet Spark", "price": 11000, "img": "https://img.automoto.ua/original/Chevrolet-Spark-2016-1e90d8ed-d48a-4950-89ef-23d249f33b1e.jpg", "inc": 0},
        {"name": "Chevrolet Gentra", "price": 16000, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_xNfU1hGv8zC19K8K3x9H7D8vE9V4L9-7pQ&s", "inc": 0},
        {"name": "Chevrolet Malibu 2", "price": 33000, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTY4Z6i-zW67HqZ9D6z5P6_YyW6U7V_I_T6uA&s", "inc": 0},
        {"name": "Ресторан 'Sky Lounge'", "price": 95000, "img": "https://images.pexels.com/photos/1579739/pexels-photo-1579739.jpeg?auto=compress&cs=tinysrgb&w=400", "inc": 250},
        {"name": "Вилла в Ташкенте", "price": 260000, "img": "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=400", "inc": 700},
        {"name": "Небоскреб City", "price": 1200000, "img": "https://images.pexels.com/photos/417273/pexels-photo-417273.jpeg?auto=compress&cs=tinysrgb&w=400", "inc": 3500}
    ]

    # Сетка магазина
    rows = [st.columns(2), st.columns(2), st.columns(2)]
    for idx, item in enumerate(items):
        col = rows[idx // 2][idx % 2]
        with col:
            st.markdown(f"<div class='shop-item'>", unsafe_allow_html=True)
            # Если картинка не загрузится, будет виден этот текст
            st.image(item['img'], use_container_width=True)
            st.markdown(f"<h3>{item['name']}</h3>", unsafe_allow_html=True)
            st.write(f"Цена: **{item['price']:,} $**")
            if item['inc'] > 0:
                st.write(f"Доход: **+{item['inc']}$/сек**")
            
            if st.button(f"Купить {item['name']}", key=f"buy_{idx}"):
                if st.session_state.money >= item['price']:
                    st.session_state.money -= item['price']
                    st.session_state.inventory.append(item['name'])
                    st.session_state.income += item['inc']
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Недостаточно денег!")
            st.markdown("</div>", unsafe_allow_html=True)

# Сброс
st.sidebar.title("Меню")
if st.sidebar.button("Сбросить прогресс 🔄"):
    st.session_state.clear()
    st.rerun()
