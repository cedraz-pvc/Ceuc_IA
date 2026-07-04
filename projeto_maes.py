# -*- coding: utf-8 -*-
"""Projeto Mães — MVP hackathon (Magalu Cloud)
Página inicial: login (dados mocados) e visão da jornada."""

import streamlit as st
from utils.auth import autenticar, barra_usuaria, USUARIOS

st.set_page_config(
    page_title="Projeto Mães", page_icon="👩‍👧", layout="centered"
)

VERDE_ESCURO = "#0F6E56"
VERDE_PASTEL = "#DFF2E9"
st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #FBFDFC; }}
      h1, h2, h3 {{ color: {VERDE_ESCURO}; }}
      div.stButton > button[kind="primary"] {{
          background-color: {VERDE_ESCURO}; border: none;
      }}
      [data-testid="stForm"] {{
          background-color: {VERDE_PASTEL};
          border-radius: 16px; border: none; padding: 24px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

barra_usuaria()

st.title("👩‍👧 Projeto Mães")
st.markdown(
    "**Da porta de volta ao mercado até o primeiro contrato — com IA e "
    "dados, no seu ritmo.**"
)

if not st.session_state.get("logada"):
    with st.form("login"):
        st.subheader("Entrar")
        email = st.text_input("E-mail", placeholder="maria@demo.com")
        senha = st.text_input("Senha", type="password", placeholder="1234")
        entrar = st.form_submit_button("Entrar", type="primary",
                                       use_container_width=True)
    if entrar:
        if autenticar(email, senha):
            st.rerun()
        else:
            st.error("E-mail ou senha inválidos.")

    with st.expander("Contas de demonstração"):
        for mail in USUARIOS:
            st.code(f"{mail}  |  senha: 1234")
else:
    st.success(f"Bem-vinda de volta, {st.session_state['nome'].split()[0]}!")
    st.markdown(
        """
        ### Sua jornada em 3 passos

        **1. 🧭 Meu perfil** — responda o questionário e nossa IA identifica
        suas habilidades e o caminho com mais chance de dar certo para o seu
        momento de vida.

        **2. 💼 Vagas para mães** — se o seu perfil for CLT, mostramos as
        empresas recrutando com flexibilidade e apoio à parentalidade,
        ordenadas pela compatibilidade com a sua rotina.

        **3. 🚀 Empreender** — se o seu perfil for empreendedora, um passo a
        passo para abrir seu negócio: tipo de empresa, formalização como MEI
        e canais de venda.

        👉 Comece pela página **Meu perfil** no menu lateral.
        """
    )
    st.info(
        "📊 A página **Evidência** mostra os dados do IBGE que motivam este "
        "projeto — aberta ao público, sem login."
    )
