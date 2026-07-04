# -*- coding: utf-8 -*-
"""Autenticação mocada para o MVP.
Em produção: streamlit-authenticator + tabela de usuárias no PostgreSQL
gerenciado da Magalu Cloud, com senha em hash (bcrypt)."""

import streamlit as st

# Usuárias de demonstração (dados fictícios)
USUARIOS = {
    "maria@demo.com": {"senha": "1234", "nome": "Maria Souza"},
    "ana@demo.com": {"senha": "1234", "nome": "Ana Oliveira"},
    "juliana@demo.com": {"senha": "1234", "nome": "Juliana Lima"},
}


def autenticar(email: str, senha: str) -> bool:
    usuario = USUARIOS.get(email.strip().lower())
    if usuario and usuario["senha"] == senha:
        st.session_state["logada"] = True
        st.session_state["email"] = email.strip().lower()
        st.session_state["nome"] = usuario["nome"]
        return True
    return False


def sair():
    for chave in ("logada", "email", "nome", "respostas", "perfil"):
        st.session_state.pop(chave, None)


def exigir_login():
    """Coloque no topo de cada página protegida."""
    if not st.session_state.get("logada"):
        st.warning("🔒 Faça login na página inicial para acessar esta área.")
        st.stop()


def barra_usuaria():
    with st.sidebar:
        if st.session_state.get("logada"):
            st.markdown(f"👩 **{st.session_state['nome']}**")
            if st.button("Sair", use_container_width=True):
                sair()
                st.rerun()
