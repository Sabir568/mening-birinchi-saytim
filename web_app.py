import streamlit as st

st.title("Mening birinchi veb-saytim! 🎉")
st.header("Python va Streamlit yordamida yaratildi")

ism = st.text_input("Ismingiz nima?")
if ism:
    st.write(f"Salom {ism}, saytimga xush kelibsiz!")
    if st.button("Xursandchilikni ko'rish"):
        st.balloons()
