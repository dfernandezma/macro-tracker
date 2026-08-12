from src.queries import (
    get_info
)

import streamlit as st

def render():
    st.title("Dashboard diario")
    
    st.text("En este apartado se muestran las macros y kcal tomadas en el día de hoy, y las restantes para llegar a tu objetivo.")

    result = get_info(st.session_state["user_id"])

    if result is None:
        st.caption("Error en el sistema. Inténtelo de nuevo más adelante.")
    else:
        bmr, kcal, protein, fat, carb = result
        st.metric("Kilocalorías objetivo",
                    kcal)
        st.metric("Proteínas objetivo",
                    protein)
        st.metric("Grasas objetivo",
                    fat)
        st.metric("Carbohidratos objetivo",
                    carb)