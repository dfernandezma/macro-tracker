from src.queries import get_info, get_current
from src.figures import progress_graph

import streamlit as st
from datetime import datetime


def render():
    st.title("Ingesta diaria")

    st.text(
        "En este apartado se muestran las macros y kcal tomadas en el día de hoy, y las restantes para llegar a tu objetivo."
    )

    result = get_info(st.session_state["user_id"])

    if result is None:
        st.caption("Error en el sistema. Inténtelo de nuevo más adelante.")
    else:
        bmr, kcal, protein, fat, carb = result

    current_result = get_current(st.session_state["user_id"], datetime.now().date())

    if current_result is None:
        st.caption("Error en el sistema. Inténtelo de nuevo más adelante")
    else:
        current_kcal, current_protein, current_fat, current_carb = current_result

        st.plotly_chart(progress_graph("Kilocalorías", kcal, current_kcal))

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.plotly_chart(progress_graph("Proteínas", protein, current_protein))
        with col2:
            st.plotly_chart(progress_graph("Grasas", fat, current_fat))
        with col3:
            st.plotly_chart(progress_graph("Carbohidratos", carb, current_carb))
