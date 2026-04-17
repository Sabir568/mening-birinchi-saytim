import streamlit as st
import random

# Sayt sarlavhasi va dizayni
st.set_page_config(page_title="Mening O'yinim", page_icon="🎮")
st.title("Soni top o'yini! 🧐")

# O'yin holatini saqlash (bu kompyuter sonni eslab qolishi uchun kerak)
if 'random_son' not in st.session_state:
    st.session_state.random_son = random.randint(1, 10)

st.write("Men 1 dan 10 gacha son o'yladim. Topa olasizmi?")

# Foydalanuvchi kiritadigan joy
taxmin = st.number_input("Soningizni kiriting:", min_value=1, max_value=10, step=1)

# Tekshirish tugmasi
if st.button("Tekshirish"):
    if taxmin == st.session_state.random_son:
        st.balloons()
        st.success(f"URAA! To'g'ri topdingiz! Men {st.session_state.random_son} sonini o'ylagan edim.")
        # Yangi o'yin uchun sonni yangilash
        if st.button("Yana o'ynash"):
            st.session_state.random_son = random.randint(1, 10)
            st.rerun()
    elif taxmin < st.session_state.random_son:
        st.warning("Kattaroq son kiriting! ⬆️")
    else:
        st.warning("Kichikroq son kiriting! ⬇️")

# Pastki qismda bezak
st.sidebar.write("---")
st.sidebar.write("Dasturchi: SabirCreator")
