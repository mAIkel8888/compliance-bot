import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# App title
st.title('Ammonia Decomposition to Hydrogen Calculator')

# User input for the amount of ammonia
amount_nh3 = st.number_input('Enter the amount of NH3 (in moles):', min_value=0.0, value=1.0)

# Stoichiometry calculations
amount_h2 = 3 * amount_nh3  # 2 NH3 produces 3 H2
amount_n2 = 0.5 * amount_nh3  # 2 NH3 produces 1 N2

# Display the calculated amounts
st.write(f"Amount of H2 produced: {amount_h2} moles")
st.write(f"Amount of N2 produced: {amount_n2} moles")

# Visualizing the reaction
fig, ax = plt.subplots()

# Bar chart for reactants and products
reactants = ['NH3']
products = ['H2', 'N2']
amounts = [amount_nh3, amount_h2, amount_n2]

ax.bar(reactants, [amount_nh3], label='Reactants', color='blue')
ax.bar(products, [amount_h2, amount_n2], label='Products', color='orange')

ax.set_ylabel('Moles')
ax.set_title('Ammonia Decomposition')
ax.legend()

st.pyplot(fig)
