import altair as alt
import pandas as pd
import streamlit as st
import math
from collections import namedtuple

def generate_spiral_data(total_points, num_turns):
    """
    Genera los puntos de datos para una espiral.

    Args:
        total_points (int): El número total de puntos a generar.
        num_turns (int): El número de vueltas en la espiral.

    Returns:
        pd.DataFrame: Un DataFrame de Pandas con las columnas 'x' e 'y'.
    """
    Point = namedtuple('Point', 'x y')
    data = []

    if num_turns == 0:
        return pd.DataFrame(data)

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    return pd.DataFrame(data)

# --- Interfaz de Usuario de Streamlit ---

st.title("Generador de Espiral Interactiva")

st.markdown(
    "Esta aplicación genera y visualiza una espiral basada en los parámetros que elijas a continuación. "
    "Usa los deslizadores para cambiar el número de puntos y vueltas."
)

# Sliders para la entrada del usuario
total_points = st.slider("Número de puntos en la espiral", 1, 5000, 2000)
num_turns = st.slider("Número de vueltas en la espiral", 1, 100, 9)

# Generar y mostrar el gráfico
if total_points > 0 and num_turns > 0:
    spiral_data = generate_spiral_data(total_points, num_turns)

    st.altair_chart(alt.Chart(spiral_data, height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'),
        use_container_width=True
    )
