# -*- coding: utf-8 -*-
"""Vagas — matching do perfil com empresas recrutando (dados mocados)."""

import streamlit as st
from utils.auth import exigir_login, barra_usuaria
from utils.branding import aplicar_marca
from utils.dados import EMPRESAS

VERDE_ESCURO = "#0F6E56"
VERDE_PASTEL = "#DFF2E9"
st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #FBFDFC; }}
      h1, h2, h3 {{ color: {VERDE_ESCURO}; }}
      .vaga-card {{
          background-color: {VERDE_PASTEL};
          border-radius: 16px; padding: 20px 24px; margin-bottom: 16px;
      }}
      .beneficio {{
          display: inline-block; background: #FFFFFF; color: {VERDE_ESCURO};
          border-radius: 999px; padding: 2px 12px; margin: 2px 4px 2px 0;
          font-size: 0.85rem;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

exigir_login()
aplicar_marca()
barra_usuaria()

st.image("assets/logo.png", width=280)
st.title("💼 Vagas para mães")

perfil = st.session_state.get("perfil")
respostas = st.session_state.get("respostas")

if not respostas:
    st.info("Responda primeiro o questionário na página **🧭 Meu perfil** — "
            "é ele que alimenta o matching.")
    st.stop()

if perfil and perfil["perfil"] == "TRANSICAO":
    st.info(
        "Seu caminho sugerido é a **🧗 Transição de carreira** — as vagas "
        "abaixo ficam mais acessíveis depois das fases de capacitação e "
        "reposicionamento da trilha. Mas explorar o mercado desde já "
        "também faz parte da jornada."
    )

if perfil and perfil["perfil"] == "EMPREENDEDORA":
    st.warning(
        "Seu perfil sugerido foi **empreendedora** — dê uma olhada na página "
        "🚀 Empreender. Mas fique à vontade para explorar as vagas também: "
        "a decisão é sempre sua."
    )


def calcular_match(vaga: dict, resp: dict) -> tuple[int, list[str]]:
    """Score 0-100 + motivos, cruzando habilidades, rotina e apoio."""
    motivos = []

    # Habilidades (peso 60)
    minhas = set(resp["habilidades"])
    pedidas = set(vaga["habilidades"])
    inter = minhas & pedidas
    pts_hab = 60 * len(inter) / len(pedidas) if pedidas else 0
    if inter:
        motivos.append("habilidades em comum: " + ", ".join(sorted(inter)))

    # Horário vs disponibilidade (peso 25)
    disp = resp["disponibilidade"]
    compat = {
        "Período integral": {"Período integral", "Meio período",
                             "Horários flexíveis"},
        "Meio período": {"Meio período", "Horários flexíveis"},
        "Horários flexíveis / por conta": {"Horários flexíveis",
                                           "Meio período"},
        "Apenas remoto": {"Horários flexíveis", "Meio período",
                          "Período integral"},
    }
    pts_hor = 0
    if vaga["horario"] in compat.get(disp, set()):
        pts_hor = 25
        motivos.append(f"horário compatível ({vaga['horario'].lower()})")
    if disp == "Apenas remoto" and vaga["modalidade"] != "Remoto":
        pts_hor = 0
        motivos.append("⚠️ vaga não é remota")

    # Apoio à parentalidade (peso 15)
    pts_apoio = 0
    precisa_apoio = resp["rede_apoio"] != "Sim, tenho com quem contar"
    tem_creche = any("creche" in b.lower() for b in vaga["beneficios"])
    flexivel = any(b.lower() in ("banco de horas", "horário flexível",
                                 "escala flexível", "home office")
                   for b in vaga["beneficios"])
    if precisa_apoio and tem_creche:
        pts_apoio += 10
        motivos.append("oferece auxílio creche")
    if flexivel:
        pts_apoio += 5

    return round(min(pts_hab + pts_hor + pts_apoio, 100)), motivos


ranqueadas = sorted(
    ((calcular_match(v, respostas), v) for v in EMPRESAS),
    key=lambda x: x[0][0], reverse=True,
)

st.markdown(
    f"Encontramos **{len(ranqueadas)} empresas recrutando** — ordenadas pela "
    "compatibilidade com as suas habilidades e a sua rotina."
)

for (score, motivos), vaga in ranqueadas:
    beneficios_html = "".join(
        f'<span class="beneficio">{b}</span>' for b in vaga["beneficios"]
    )
    st.markdown(
        f"""
        <div class="vaga-card">
          <strong style="font-size:1.1rem;">{vaga['vaga']}</strong><br>
          {vaga['empresa']} · {vaga['setor']} · {vaga['cidade']}<br>
          <em>{vaga['modalidade']} · {vaga['horario']}</em><br>
          {beneficios_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(score / 100, text=f"Compatibilidade: {score}%")
    if motivos:
        st.caption("Por quê: " + "; ".join(motivos) + ".")
    if st.button("📨 Enviar meu perfil", key=vaga["empresa"] + vaga["vaga"]):
        st.success(
            f"Perfil enviado para **{vaga['empresa']}**! (No MVP isso é "
            "simulado — em produção, dispara a candidatura via integração "
            "com o ATS da empresa.)"
        )
    st.divider()

st.caption(
    "💡 Você sabia? É proibido por lei (Lei 9.029/95) exigir teste de "
    "gravidez ou perguntar sobre planos de filhos em processo seletivo. "
    "Conhecer seus direitos também é preparação para entrevista."
)
