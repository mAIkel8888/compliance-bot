import streamlit as st
import pandas as pd

st.title("Material Stock Manager")

# Initialize session state for materials
if 'materials' not in st.session_state:
    st.session_state.materials = {}

MATERIAL_OPTIONS = [
    "Piedra Caliza",
    "Durmientes de Madera",
    "Malla de Acero",
]

st.header("Add a new material")
with st.form("add_material"):
    name = st.selectbox("Material", MATERIAL_OPTIONS)
    qty = st.number_input("Initial quantity", min_value=0, step=1, value=0)
    submitted = st.form_submit_button("Add/Update")
    if submitted:
        current = st.session_state.materials.get(name, 0)
        st.session_state.materials[name] = current + int(qty)

if st.session_state.materials:
    st.header("Adjust stock")
    with st.form("adjust_stock"):
        material = st.selectbox("Select material", list(st.session_state.materials.keys()))
        delta = st.number_input("Add/Subtract quantity", value=0, step=1, format="%d")
        adjust = st.form_submit_button("Apply")
        if adjust:
            st.session_state.materials[material] += int(delta)
            if st.session_state.materials[material] < 0:
                st.session_state.materials[material] = 0

    st.header("Current stock")
    df = pd.DataFrame({
        'Material': list(st.session_state.materials.keys()),
        'Quantity': list(st.session_state.materials.values())
    })
    st.dataframe(df.set_index('Material'))
    st.bar_chart(df.set_index('Material'))
else:
    st.info("No materials in stock. Add materials above.")
