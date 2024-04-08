#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import numpy as np
import pprint
import pandas as pd
import time
# import plotly.graph_objects as go

# empty dataframe hidden until user inputs data
df = pd.DataFrame()


st.title('CSE Calcul ASC 2024')
st.write('')

# add some space between photo and instructions
st.write('')
st.subheader('vous pouvez saisir vos informations pour le calcul ASC')


# create placeholders to clear inputs when clicking "start over" button
placeholder_c = st.empty()
placeholder_s = st.empty()



# In[9]:


# have user input the amount they have for each coin

userRFF = placeholder_c.number_input('Revenu fiscal de reference 2024 (sur les revenus 2023) en euros: ', min_value= 0, value=100000)
userNBPart = placeholder_s.number_input('Nombre de parts ', min_value= 1.,format="%.2f", step=0.5)



# In[ ]:


# tell user how much they have in gold pieces

QF = (userRFF / userNBPart / 12) 
QF = round(QF)

st.write(f'Votre Quotient Familial {QF:,d} .')


# In[ ]:


st.write('')

if QF > 2300:
    st.subheader('Vous avez l\'enveloppe standard de 193 euros.')
    st.write('Pas besoin de venir nous voir :) ')
elif 2050 < QF <= 2300 :
    st.subheader('Vous avez une enveloppe de 250 euros.')
    st.write('Vous pouvez venir nous voir!! :) ')
    st.write('Nous avons besoin de votre avis d\'imposition pour valider cette enveloppe. ')
elif 1800 < QF <= 2050 :
    st.subheader('Vous avez une enveloppe de 300 euros.')
    st.write('Vous pouvez venir nous voir!! :) ')
    st.write('Nous avons besoin de votre avis d\'imposition pour valider cette enveloppe. ')
elif 1550 < QF <= 1800:
    st.subheader('Vous avez une enveloppe de 350 euros.')
    st.write('Vous pouvez venir nous voir!! :) ')
    st.write('Nous avons besoin de votre avis d\'imposition pour valider cette enveloppe. ')
elif 1300 < QF <= 1550:
    st.subheader('Vous avez une enveloppe de 400 euros.')
    st.write('Vous pouvez venir nous voir!! :) ')
    st.write('Nous avons besoin de votre avis d\'imposition pour valider cette enveloppe. ')
elif QF <= 1300:
    st.subheader('Vous avez une enveloppe de 450 euros.')
    st.write('Vous pouvez venir nous voir!! :) ')
    st.write('Nous avons besoin de votre avis d\'imposition pour valider cette enveloppe. ')
else: 
    st.write('Vous avez une enveloppe bonifiée.')
    st.write('Vous pouvez venir nous voir!! :) ')



# In[ ]:


# create dividing line to separate calculations from reset
st.write('-------------------------')






