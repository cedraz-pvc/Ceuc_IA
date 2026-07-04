# -*- coding: utf-8 -*-
"""Meu perfil — questionário e classificação por IA (CLT vs Empreendedora)."""

import streamlit as st
from utils.auth import exigir_login, barra_usuaria
from utils.branding import aplicar_marca
from utils.ia import classificar_perfil

VERDE_ESCURO = "#0F6E56"
VERDE_PASTEL = "#DFF2E9"
st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #FBFDFC; }}
      h1, h2, h3 {{ color: {VERDE_ESCURO}; }}
      [data-testid="stForm"] {{
          background-color: {VERDE_PASTEL};
          border-radius: 16px; border: none; padding: 24px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

exigir_login()
aplicar_marca()
barra_usuaria()

st.image("assets/logo.png", width=280)
st.title("🧭 Meu perfil")
st.markdown(
    "Responda com calma — não existe resposta certa. A IA usa essas "
    "informações para sugerir o caminho **mais compatível com a sua vida "
    "hoje**, não um julgamento sobre você."
)

HABILIDADES = [
    "Organização", "Atendimento ao cliente", "Negociação", "Redes sociais",
    "Excel / planilhas", "Gestão do tempo", "Liderança", "Criatividade",
    "Culinária", "Costura", "Beleza e estética", "Artesanato",
    "Cuidado infantil", "Informática", "Escrita e comunicação",
]

with st.form("questionario"):
    st.subheader("Sobre a sua trajetória")
    escolaridade = st.selectbox(
        "Escolaridade",
        ["Fundamental", "Médio", "Técnico", "Superior", "Pós-graduação"],
        index=1,
    )
    areas = st.multiselect(
        "Em quais áreas você já trabalhou (ou trabalha)?",
        ["Administrativo", "Vendas", "Educação / cuidado", "Saúde",
         "Tecnologia", "Financeiro", "Alimentação", "Beleza / estética",
         "Serviços domésticos", "Comunicação / marketing", "Nunca trabalhei"],
    )
    anos_experiencia = st.slider("Anos de experiência formal (com carteira)",
                                 0, 30, 2)
    tempo_fora = st.slider("Há quanto tempo está fora do mercado? (anos)",
                           0, 15, 1)
    habilidades = st.multiselect(
        "Quais habilidades você tem? (marque todas que se aplicam)",
        HABILIDADES,
    )

    st.subheader("Sobre a sua rotina")
    idade_filho = st.selectbox(
        "Idade do seu filho mais novo",
        ["0 a 1 ano", "2 a 3 anos", "4 a 5 anos", "6 anos ou mais"],
    )
    rede_apoio = st.radio(
        "Você tem com quem deixar seus filhos para trabalhar?",
        ["Sim, tenho com quem contar", "Só em parte do dia", "Não tenho"],
    )
    disponibilidade = st.radio(
        "Qual disponibilidade combina com a sua rotina?",
        ["Período integral", "Meio período", "Horários flexíveis / por conta",
         "Apenas remoto"],
    )

    st.subheader("Sobre o que você quer")
    autonomia = st.select_slider(
        "O que pesa mais para você?",
        options=["1", "2", "3", "4", "5"], value="3",
        help="1 = estabilidade e benefícios | 5 = autonomia total de horários",
    )
    st.caption("1 = estabilidade e benefícios · 5 = autonomia de horários")
    apetite_risco = st.select_slider(
        "Como você lida com renda variável?",
        options=["1", "2", "3", "4", "5"], value="2",
        help="1 = preciso de renda fixa | 5 = topo variação se o teto for maior",
    )
    st.caption("1 = preciso de renda fixa · 5 = topo renda variável")
    ja_vendeu = st.radio(
        "Você já vendeu produtos ou serviços por conta própria?",
        ["Sim", "Não"],
    )
    objetivo_carreira = st.radio(
        "Pensando na sua volta ao mercado, você quer...",
        ["Voltar para a área em que já atuava", "Quero mudar de área",
         "Ainda não sei"],
    )
    renda_objetivo = st.selectbox(
        "Qual renda mensal você busca?",
        ["Até R$ 2.000", "R$ 2.000 a R$ 5.000", "R$ 5.000 a R$ 8.000",
         "Acima de R$ 8.000"],
    )

    enviar = st.form_submit_button("✨ Descobrir meu caminho",
                                   type="primary", use_container_width=True)

if enviar:
    if not habilidades:
        st.warning("Marque pelo menos uma habilidade — você tem várias!")
        st.stop()

    respostas = {
        "escolaridade": escolaridade,
        "areas_experiencia": areas,
        "anos_experiencia": anos_experiencia,
        "tempo_fora_mercado_anos": tempo_fora,
        "habilidades": habilidades,
        "idade_filho_mais_novo": idade_filho,
        "rede_apoio": rede_apoio,
        "disponibilidade": disponibilidade,
        "autonomia": autonomia,
        "apetite_risco": apetite_risco,
        "ja_vendeu": ja_vendeu,
        "objetivo_carreira": objetivo_carreira,
        "renda_objetivo": renda_objetivo,
    }
    with st.spinner("A IA está analisando o seu perfil..."):
        resultado = classificar_perfil(respostas)

    st.session_state["respostas"] = respostas
    st.session_state["perfil"] = resultado

if st.session_state.get("perfil"):
    r = st.session_state["perfil"]
    st.divider()

    if r["perfil"] == "CLT":
        st.success(
            f"### 💼 Seu caminho sugerido: **vaga CLT**\n\n"
            f"{r['justificativa']}"
        )
        destino = "💼 Vagas"
    elif r["perfil"] == "TRANSICAO":
        st.success(
            f"### 🧗 Seu caminho sugerido: **transição de carreira**\n\n"
            f"{r['justificativa']}"
        )
        destino = "🧗 Transição"
    else:
        st.success(
            f"### 🚀 Seu caminho sugerido: **empreender**\n\n"
            f"{r['justificativa']}"
        )
        destino = "🚀 Empreender"

    st.progress(r["confianca"] / 100,
                text=f"Confiança da análise: {r['confianca']}%")

    st.markdown("**Suas habilidades em destaque:**")
    st.markdown(" ".join(f"`{h}`" for h in r["habilidades_destaque"]))

    st.markdown("**Próximos passos recomendados:**")
    for rec in r["recomendacoes"]:
        st.markdown(f"- {rec}")

    origem = ("modelo de linguagem" if r.get("origem") == "llm"
              else "análise heurística (LLM offline)")
    st.caption(f"Análise gerada por: {origem}. Você pode refazer o "
               "questionário quando quiser — seu momento muda, o caminho "
               "também pode mudar.")

    st.info(f"👉 Continue na página **{destino}** no menu lateral.")
