import streamlit as st
import time

# Настройки сайта
st.set_page_config(page_title="Симулятор Миллионера 💼", page_icon="💰", layout="wide")

# --- СТИЛИ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .money-display {
        font-size: 55px; font-weight: bold; color: #00FF00;
        text-align: center; border: 3px solid #00FF00;
        border-radius: 20px; padding: 10px; margin-bottom: 25px;
        background: rgba(0, 255, 0, 0.05);
    }
    .card {
        background-color: #1E1E1E; padding: 15px;
        border-radius: 15px; border: 1px solid #333;
        margin-bottom: 20px; text-align: center;
    }
    .inventory-card {
        background-color: #262730; padding: 10px;
        border-radius: 10px; border-left: 5px solid #00FF00;
        margin-bottom: 10px; display: flex; align-items: center; gap: 20px;
    }
    .img-main { border-radius: 10px; width: 100%; height: 160px; object-fit: cover; }
    .img-inv { border-radius: 5px; width: 80px; height: 50px; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click_power' not in st.session_state: st.session_state.click_power = 50
if 'passive' not in st.session_state: st.session_state.passive = 0
if 'inventory_list' not in st.session_state: st.session_state.inventory_list = []
if 'last_time' not in st.session_state: st.session_state.last_time = time.time()

# Пассивный доход
now = time.time()
diff = now - st.session_state.last_time
if diff >= 1:
    st.session_state.money += int(diff * st.session_state.passive)
    st.session_state.last_time = now

# --- БАЗА ДАННЫХ ТОВАРОВ ---
SHOP_ITEMS = [
    {
        "id": 1, "name": "Chevrolet Spark", "price": 10000, "type": "Авто", 
        "img": "https://upload.wikimedia.org/wikipedia/commons/e/e3/2016_Chevrolet_Spark.jpg", "income": 0
    },
    {
        "id": 2, "name": "Chevrolet Gentra", "price": 15000, "type": "Авто", 
        "img": "https://autostrada.uz/wp-content/uploads/2021/09/gentra-black.jpg", "income": 0
    },
    {
        "id": 3, "name": "Chevrolet Malibu 2", "price": 32000, "type": "Авто", 
        "img": "https://motor.uz/files/cache/motor.uz/uploads/malibu/original/5e3b5e4368153_main_image.jpg", "income": 0
    },
    {
        "id": 4, "name": "Ресторан", "price": 80000, "type": "Бизнес", 
        "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400", "income": 150
    },
    {
        "id": 5, "name": "Квартира в Tashkent City", "price": 200000, "type": "Жилье", 
        "img": "https://tashkentcity.uz/storage/photos/shares/banners/banner_3.jpg", "income": 400
    },
    {
        "id": 6, "name": "Загородная Вилла", "price": 500000, "type": "Жилье", 
        "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400", "income": 1200
    }
]

# --- ИНТЕРФЕЙС ---
st.markdown(f"<div class='money-display'>{st.session_state.money:,.0f} $</div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.5, 2.5])

# --- ЛЕВАЯ ПАНЕЛЬ: РАБОТА И ГАРАЖ ---
with col_left:
    st.header("💼 Работа")
    if st.button("ЗАРАБОТАТЬ ДЕНЬГИ 💵", use_container_width=True):
        st.session_state.money += st.session_state.click_power
        st.rerun()
    
    st.write("---")
    st.header("📦 Моё Имущество")
    if not st.session_state.inventory_list:
        st.info("Вы пока ничего не купили.")
    else:
        for item in st.session_state.inventory_list:
            st.markdown(f"""
                <div class='inventory-card'>
                    <img src='{item['img']}' class='img-inv'>
                    <div>
                        <b>{item['name']}</b><br>
                        <small>{item['type']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- ПРАВАЯ ПАНЕЛЬ: МАГАЗИН ---
with col_right:
    st.header("🏪 Магазин")
    
    tabs = st.tabs(["🚗 Автомобили", "🏠 Недвижимость"])
    
    with tabs[0]: # Авто
        cols = st.columns(2)
        cars = [i for i in SHOP_ITEMS if i['type'] == "Авто"]
        for idx, car in enumerate(cars):
            with cols[idx % 2]:
                st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<img src='{car['img']}' class='img-main'>", unsafe_allow_html=True)
                st.subheader(car['name'])
                st.write(f"Цена: **{car['price']:,} $**")
                if st.button(f"Купить {car['name']}", key=f"buy_{car['id']}"):
                    if st.session_state.money >= car['price']:
                        st.session_state.money -= car['price']
                        st.session_state.inventory_list.append(car)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Недостаточно денег!")
                st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]: # Недвижимость
        cols = st.columns(2)
        houses = [i for i in SHOP_ITEMS if i['type'] != "Авто"]
        for idx, house in enumerate(houses):
            with cols[idx % 2]:
                st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<img src='{house['img']}' class='img-main'>", unsafe_allow_html=True)
                st.subheader(house['name'])
                st.write(f"Цена: **{house['price']:,} $**")
                st.write(f"Доход: **+{house['income']}$/сек**")
                if st.button(f"Купить {
