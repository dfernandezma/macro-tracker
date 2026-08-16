import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.queries import get_records, get_foods, add_food

import streamlit as st
import pandas as pd
from datetime import datetime


def render():
    st.title("Registro de Comidas Diario")

    tab_record, tab_add = st.tabs(["Registro diario", "Añadir comida"])

    with tab_record:
        with st.form("form_record"):
            records = get_records(st.session_state["user_id"], datetime.now().date())

            if records is None:
                st.caption(
                    "Error en el sistema obteniendo registros diarios. Inténtelo de nuevo más adelante."
                )
            else:
                st.dataframe(records, hide_index=True)

    with tab_add:
        with st.form("form_register"):
            foods = get_foods()

            food = st.selectbox("Alimento", options=foods.keys())
            amount = st.number_input(
                "Cantidad (g)", min_value=0.0, max_value=5000.0, value=100.0, step=0.01
            )

            register_food_button = st.form_submit_button(
                "Añadir comida", type="primary"
            )

            if register_food_button:
                record_id = add_food(
                    st.session_state["user_id"], foods[food], amount, datetime.now()
                )

                if record_id is None:
                    st.caption(
                        "Error en el sistema, no se pudo insertar la comida. Inténtelo de nuevo más adelante..."
                    )
                else:
                    st.success("¡Comida añadida correctamente!")