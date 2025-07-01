import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mensagem de Tracking", page_icon="🚀")

st.title("Mensagem de Tracking para Clientes 🚀")

code = st.text_input("Insere o código de tracking:")

if code:
    message = f"""Boas, os stickers já vão a caminho! 🚀

Fica aqui o tracking http://ctt.pt/t/{code}"""

    st.text_area("Mensagem pronta para enviar:", value=message, height=100, label_visibility="visible")

    # Styled copy button with native look
    components.html(f"""
    <div style="text-align: center; margin-top: 1em;">
        <button 
            onclick="navigator.clipboard.writeText(`{message}`); alert('Mensagem copiada! ✅');" 
            style="
                background-color: #f63366;
                color: white;
                padding: 0.6em 1.2em;
                border: none;
                border-radius: 0.4em;
                font-size: 1em;
                cursor: pointer;
            "
        >
            Copiar mensagem
        </button>
    </div>
    """, height=100)
