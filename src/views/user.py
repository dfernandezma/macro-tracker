import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.queries import modify_user, get_user_info
from src.auth import verify_email
from src.constants import MAP_ACTIVITY, MAP_ACTIVITY_NUM, MAP_OBJETIVES, MAP_SEX

import streamlit as st


def render():
    st.title("Perfil de usuario")
    st.subheader("Modificar datos personales")

    if "form_key_counter" not in st.session_state:
        st.session_state["form_key_counter"] = 0

    with st.form(f"form_modify_{st.session_state['form_key_counter']}"):
        current_info = get_user_info(st.session_state["user_id"])

        if current_info is None:
            st.caption(
                "No se pudo obtener información de usuario. Por favor, inténtelo de nuevo más adelante..."
            )
        else:
            (
                current_sex,
                current_age,
                current_height,
                current_weight,
                current_activity,
                current_objective,
            ) = current_info

            suffix = st.session_state["form_key_counter"]

            sex = st.selectbox(
                "Sexo:",
                options=list(MAP_SEX.keys()),
                format_func=lambda x: MAP_SEX[x],
                index=list(MAP_SEX.keys()).index(current_sex),
                key=f"mod_sex_{suffix}",
            )
            age = st.number_input(
                "Edad:",
                min_value=12,
                max_value=90,
                value=current_age,
                step=1,
                key=f"mod_age_{suffix}",
            )
            weight = st.number_input(
                "Peso (kg):",
                min_value=10.0,
                max_value=250.0,
                value=current_weight,
                step=0.01,
                key=f"mod_weight_{suffix}",
            )
            height = st.number_input(
                "Altura (cm)",
                min_value=90,
                max_value=230,
                value=current_height,
                step=1,
                key=f"mod_height_{suffix}",
            )

            st.divider()

            st.text("Objetivos y actividad")
            activity = st.selectbox(
                "Nivel de actividad",
                options=list(MAP_ACTIVITY.keys()),
                format_func=lambda x: MAP_ACTIVITY[x],
                index=list(MAP_ACTIVITY.keys()).index(current_activity),
                key=f"mod_act_{suffix}",
            )
            objective = st.selectbox(
                "Objetivo:",
                options=list(MAP_OBJETIVES.keys()),
                format_func=lambda x: MAP_OBJETIVES[x],
                index=list(MAP_OBJETIVES.keys()).index(current_objective),
                key=f"mod_obj_{suffix}",
            )

            modify_button = st.form_submit_button("Confirmar cambios", type="primary")

            if modify_button:
                modified_id = modify_user(
                    st.session_state["user_id"],
                    age,
                    sex,
                    height,
                    weight,
                    activity,
                    objective,
                )

                if modified_id is None:
                    st.caption("Error del sistema. Inténtelo de nuevo más adelante...")
                else:
                    st.success("¡Datos actualizados correctamente!")

            restart_button = st.form_submit_button("Reestablecer", type="secondary")

            if restart_button:
                st.session_state["form_key_counter"] += 1
                st.rerun()
