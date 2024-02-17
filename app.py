import streamlit as st
from dotenv import load_dotenv
import auth
from panels import show_panels
from database import create_server_connection, get_clientes
from styles import load_styles

st.markdown(load_styles(), unsafe_allow_html=True)

# Función para manejar el inicio de sesión
def handle_login():
    with st.form(key='login_form'):
        login_username = st.text_input("Nombre de Usuario", key="login_username")
        login_password = st.text_input("Contraseña", type="password", key="login_password")
        submit_button = st.form_submit_button(label="Iniciar Sesión")
        
        if submit_button:
            if auth.verify_login(login_username, login_password):
                st.session_state['logged_in'] = True
                st.success("Inicio de sesión exitoso")
                return True
            else:
                st.error("Error en el inicio de sesión")
                return False
    return False

# Función para manejar el cierre de sesión
def handle_logout():
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']  # Elimina el estado de inicio de sesión
    if 'selected_cliente_id' in st.session_state:
        del st.session_state['selected_cliente_id']  # Elimina el cliente seleccionado si existe

# Función principal
def main():
    st.title("Sistema de Facturación")

    # Carga variables de entorno
    load_dotenv()

    if not st.session_state.get('logged_in'):
        st.subheader("Iniciar Sesión")
        if handle_login():
            st.experimental_rerun()  # Re-ejecuta el script para actualizar la interfaz
             
    else:
        selected_panel = show_panels(st)  # Función para mostrar los paneles de la aplicación
        if st.sidebar.button("Cerrar Sesión"):
            auth.logout()
            handle_logout()  # Limpia la sesión y el estado
            st.experimental_rerun()  # Re-ejecuta el script para regresar a la página de inicio de sesión
            st.success("Sesión cerrada correctamente")  # Muestra un mensaje de confirmación

if __name__ == "__main__":
    main()
