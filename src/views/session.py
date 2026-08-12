import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.auth import (
    verify_email,
    login_user,
    register_user
)
from src.constants import (
    MAP_ACTIVITY,
    MAP_OBJETIVES,
    MAP_SEX
)

import streamlit as st

def render():
    st.title("Macro-Tracker")

    tab_login, tab_register = st.tabs(["Iniciar Sesión", "Registrarse"])

    with tab_login:
        st.subheader("Accede a tu cuenta")

        with st.form("form_login"):
            email_login = st.text_input("Correo electrónico:")
            passwd_login = st.text_input("Contraseña:",
                                         type="password")

            login_button = st.form_submit_button("Login",
                                                type="primary")

            if login_button:
                if not verify_email(email_login):
                    st.caption("No existe ninguna cuenta con ese correo electrónico.")

                user_id = login_user(email_login, passwd_login)

                if user_id is None:
                    st.caption("Contraseña incorrecta. Pruebe de nuevo")
                else:
                    st.session_state["user_id"] = user_id

    with tab_register:
        st.subheader("Crea una cuenta nueva")

        with st.form("form_register"):
            st.text("Información de cuenta")
            email_register = st.text_input("Correo electrónico:")
            passwd_register = st.text_input("Contraseña:",
                                            type="password")

            st.divider()

            st.text("Información personal")
            sex = st.selectbox("Sexo:",
                               options=list(MAP_SEX.keys()),
                               format_func=lambda x: MAP_SEX[x])
            age = st.number_input("Edad:",
                                  min_value=12,
                                  max_value=90,
                                  value=18,
                                  step=1)
            weight = st.number_input("Peso (kg):",
                                     min_value=10.0,
                                     max_value=250.0,
                                     value=70.0,
                                     step=0.01)
            height = st.number_input("Altura (cm)",
                                     min_value=90,
                                     max_value=230,
                                     value=170,
                                     step=1)

            st.divider()

            st.text("Objetivos y actividad")
            activity = st.selectbox("Nivel de actividad",
                                    options=list(MAP_ACTIVITY.keys()),
                                    format_func=lambda x: MAP_ACTIVITY[x])
            objective = st.selectbox("Objetivo:",
                                     options=list(MAP_OBJETIVES.keys()),
                                     format_func=lambda x: MAP_OBJETIVES[x])

            register_button = st.form_submit_button("Registrarse",
                                                    type="primary")

            if register_button:
                if verify_email(email_register):
                    st.caption("Ya existe una cuenta con este correo")
                else:
                    user_id = register_user(email_register, passwd_register, sex, activity, objective, height, age, weight)

                    if user_id is None:
                        st.caption("Error del sistema. Inténtelo de nuevo más adelante...")
                    else:
                        st.session_state["user_id"] = user_id