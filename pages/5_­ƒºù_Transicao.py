# -*- coding: utf-8 -*-
"""Transição de carreira — trilha objetiva em 5 fases, com checklist,
progresso e a próxima ação sempre em destaque."""

import streamlit as st
from utils.auth import exigir_login, barra_usuaria
from utils.branding import aplicar_marca
from utils.dados import CURSOS_POR_AREA
from utils.ia import gerar_resumo

VERDE_ESCURO = "#0F6E56"
VERDE_PASTEL = "#DFF2E9"
LARANJA = "#D85A30"
st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #FBFDFC; }}
      h1, h2, h3 {{ color: {VERDE_ESCURO}; }}
      .fase {{
          background-color: {VERDE_PASTEL};
          border-radius: 16px; padding: 18px 22px; margin-bottom: 8px;
      }}
      .proxima {{
          background-color: #FDEEE7; border-left: 6px solid {LARANJA};
          border-radius: 0; padding: 16px 20px; margin: 12px 0;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

exigir_login()
aplicar_marca()
barra_usuaria()

st.image("assets/logo.png", width=280)
st.title("🧗 Transição de carreira")

respostas = st.session_state.get("respostas")
if not respostas:
    st.info("Responda primeiro o questionário na página **🧭 Meu perfil** — "
            "é ele que personaliza a sua trilha.")
    st.stop()

st.markdown(
    "Mudar de área não é começar do zero: é **reposicionar** o que você já "
    "tem. Esta trilha organiza a mudança em 5 fases. Faça na ordem, marque "
    "o que concluir e siga a próxima ação — uma por vez."
)

# ------------------ Área-alvo (decisão da Fase 1) ---------------------
area_alvo = st.selectbox(
    "🎯 Sua área-alvo (a decisão mais importante da trilha):",
    list(CURSOS_POR_AREA.keys()),
    key="area_alvo",
)

habilidades = respostas.get("habilidades", [])
if habilidades:
    st.markdown(
        "**Suas habilidades transferíveis** (você leva isso com você para "
        "qualquer área): " + " ".join(f"`{h}`" for h in habilidades)
    )

# ------------------------- As 5 fases ---------------------------------
FASES = [
    ("Fase 1 · Diagnóstico", "2 a 3 dias", [
        "Escolher UMA área-alvo (o seletor acima) e não trocar por 90 dias",
        "Listar 3 habilidades que você já tem e que a área-alvo valoriza",
        "Definir a meta: 'estar empregada/atuando na área X em N meses'",
    ]),
    ("Fase 2 · Capacitação", "4 a 8 semanas", [
        "Matricular-se em 1 curso gratuito da área-alvo (lista abaixo)",
        "Estudar 30-60 min por dia (constância > intensidade)",
        "Concluir e guardar o certificado do primeiro curso",
        "Fazer 1 pequeno projeto prático para mostrar (portfólio simples)",
    ]),
    ("Fase 3 · Reposicionamento", "1 semana", [
        "Gerar seu novo resumo profissional (botão da IA abaixo)",
        "Atualizar o currículo: habilidades transferíveis no topo",
        "Atualizar o LinkedIn: título com a ÁREA-ALVO, não a antiga",
        "Pedir a 2 pessoas próximas para revisar seu currículo",
    ]),
    ("Fase 4 · Rede e mercado", "contínua", [
        "Avisar sua rede que está em transição (post ou mensagens diretas)",
        "Entrar em 1 comunidade de mães profissionais (ex.: grupos locais, "
        "B2Mamy, Maternativa)",
        "Conversar com 2 pessoas que já atuam na área-alvo (café virtual)",
    ]),
    ("Fase 5 · Candidaturas", "2 a 4 semanas", [
        "Candidatar-se a 5 vagas por semana (use a página 💼 Vagas)",
        "Adaptar o resumo para cada vaga (2 linhas mudam tudo)",
        "Preparar respostas para o gap: maternidade como competência",
        "Revisar seus direitos antes das entrevistas (Lei 9.029/95)",
    ]),
]

# Checklist com estado por usuária
email = st.session_state.get("email", "anon")
total, feitos = 0, 0
proxima_acao = None

for i, (titulo, prazo, acoes) in enumerate(FASES):
    st.markdown(f'<div class="fase"><strong>{titulo}</strong> · '
                f'prazo sugerido: {prazo}</div>', unsafe_allow_html=True)
    for j, acao in enumerate(acoes):
        chave = f"trilha_{email}_{i}_{j}"
        marcado = st.checkbox(acao, key=chave)
        total += 1
        if marcado:
            feitos += 1
        elif proxima_acao is None:
            proxima_acao = (titulo, acao)

    # Conteúdo de apoio contextual por fase
    if i == 1:
        with st.expander(f"📚 Cursos gratuitos para {area_alvo}"):
            for curso in CURSOS_POR_AREA[area_alvo]:
                st.markdown(f"- {curso}")
    if i == 2:
        with st.expander("✨ Gerar meu resumo profissional com IA"):
            st.caption(
                "A IA traduz o período da maternidade em competências — "
                "sem escondê-lo — e conecta suas habilidades à área-alvo."
            )
            if st.button("Gerar resumo", type="primary"):
                with st.spinner("Escrevendo o seu resumo..."):
                    resumo = gerar_resumo(respostas, area_alvo)
                st.session_state["resumo_gerado"] = resumo
            if st.session_state.get("resumo_gerado"):
                st.text_area(
                    "Copie e ajuste com as suas palavras:",
                    st.session_state["resumo_gerado"], height=180,
                )

# ------------------------- Progresso ----------------------------------
st.divider()
progresso = feitos / total if total else 0
st.progress(progresso, text=f"Progresso da trilha: {feitos} de {total} "
            f"ações ({progresso:.0%})")

if proxima_acao:
    st.markdown(
        f"""
        <div class="proxima">
          <strong>👉 Sua próxima ação ({proxima_acao[0]}):</strong><br>
          {proxima_acao[1]}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.balloons()
    st.success(
        "🎉 Trilha concluída! Você não está mais 'em transição' — você "
        "chegou. Mantenha o ritmo de candidaturas na página 💼 Vagas e "
        "continue nutrindo a rede da Fase 4."
    )

st.caption(
    "No MVP, o progresso vale para a sessão atual. Em produção, ele é "
    "salvo no PostgreSQL da Magalu Cloud e a mãe recebe lembretes da "
    "próxima ação por WhatsApp/e-mail."
)
