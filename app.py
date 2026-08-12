from src.views import session
from src.queries import (
    get_info,
)

import streamlit as st

def main():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None

    if st.session_state["user_id"] == None:
        session.render()
    else:
        st.sidebar.title("Menú Principal")
        menu = st.sidebar.radio("Ir a:",
                                options=["Dashboard", "Añadir Comida", "Mi Perfil"])

        if menu == "Dashboard":
            dashboard.render()

if __name__ == "__main__":
    main()