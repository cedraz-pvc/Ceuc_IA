# -*- coding: utf-8 -*-
"""Empreender — trilha de formalização e escolha do tipo de negócio."""

import streamlit as st
from utils.auth import exigir_login, barra_usuaria
from utils.branding import aplicar_marca
from utils.dados import NEGOCIOS_POR_HABILIDADE, NEGOCIO_PADRAO, PASSOS_MEI

VERDE_ESCURO = "#0F6E56"
VERDE_PASTEL = "#DFF2E9"
st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #FBFDFC; }}
      h1, h2, h3 {{ color: {VERDE_ESCURO}; }}
      .passo {{
          background-color: {VERDE_PASTEL};
          border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

exigir_login()
aplicar_marca()
barra_usuaria()

st.image("assets/logo.png", width=280)
st.title("🚀 Empreender")

perfil = st.session_state.get("perfil")
respostas = st.session_state.get("respostas")

if not respostas:
    st.info("Responda primeiro o questionário na página **🧭 Meu perfil** — "
            "é ele que personaliza esta trilha.")
    st.stop()

if perfil and perfil["perfil"] == "CLT":
    st.warning(
        "Seu perfil sugerido foi **CLT** — veja a página 💼 Vagas. Mas se "
        "empreender é um sonho, esta trilha continua toda sua."
    )

# ------------------- Que negócio combina com você -------------------
st.header("1. Que negócio combina com você")

sugestoes = [
    NEGOCIOS_POR_HABILIDADE[h]
    for h in respostas["habilidades"]
    if h in NEGOCIOS_POR_HABILIDADE
] or [NEGOCIO_PADRAO]

for s in sugestoes[:3]:
    st.markdown(
        f"""
        <div class="passo">
          <strong>{s['negocio']}</strong><br>
          CNAE de referência: <code>{s['cnae_exemplo']}</code><br>
          Canal de venda sugerido: {s['canal']}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "As sugestões partem das habilidades que você marcou no questionário. "
    "O CNAE é o código da atividade econômica — confirme no Portal do "
    "Empreendedor se a ocupação é permitida ao MEI."
)

# ----------------------- MEI ou outro formato -----------------------
st.header("2. MEI ou outro formato?")

renda = respostas["renda_objetivo"]
if renda == "Acima de R$ 8.000":
    st.warning(
        "⚠️ Sua meta de renda pode ultrapassar o teto do MEI "
        "(R$ 81.000/ano ≈ R$ 6.750/mês de faturamento). Nesse cenário, o "
        "caminho é abrir uma **ME (Microempresa) no Simples Nacional** — "
        "vale conversar com um contador, e muitos atendem online com "
        "mensalidade acessível. Comece como MEI se o faturamento inicial "
        "for menor e migre quando crescer: a migração é um bom problema "
        "para se ter. 😉"
    )
else:
    st.success(
        "✅ Para a sua meta de renda, o **MEI** é o formato ideal: "
        "formalização gratuita, imposto fixo mensal baixo e direitos "
        "previdenciários — incluindo **salário-maternidade** para as "
        "próximas fases da vida, aposentadoria e auxílio-doença."
    )

with st.expander("Entenda o MEI em 30 segundos"):
    st.markdown(
        """
        - **Quem pode:** faturamento até R$ 81.000/ano, sem participação em
          outra empresa, no máximo 1 funcionário, atividade na lista permitida.
        - **Quanto custa:** uma guia mensal fixa (DAS), na faixa de R$ 70-80
          conforme a atividade — já inclui INSS.
        - **O que você ganha:** CNPJ (para emitir nota, vender em marketplace
          e abrir conta PJ), cobertura do INSS e acesso a crédito com juros
          menores que pessoa física.
        - **Obrigações:** pagar o DAS até o dia 20 e entregar uma declaração
          anual simples (DASN-SIMEI) até 31 de maio.

        *Valores e limites vigentes na criação deste MVP — o app em produção
        consulta a base atualizada.*
        """
    )

# ----------------------- Passo a passo ------------------------------
st.header("3. Passo a passo para abrir seu MEI")

for i, (titulo, detalhe) in enumerate(PASSOS_MEI, start=1):
    st.markdown(
        f"""
        <div class="passo">
          <strong>Passo {i} — {titulo}</strong><br>{detalhe}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.error(
    "🚨 **Atenção a golpes:** a formalização do MEI é 100% gratuita e feita "
    "apenas no portal oficial **gov.br/mei**. Sites que cobram taxa de "
    "abertura são intermediários desnecessários — alguns, golpes."
)

# ----------------------- Primeiros passos de gestão ------------------
st.header("4. Seu negócio de pé: os 3 hábitos que separam quem cresce")

st.markdown(
    """
    **Separe as finanças.** Conta do negócio ≠ conta da casa. Defina um
    "salário" seu (pró-labore) e registre toda entrada e saída — uma
    planilha simples resolve no começo.

    **Precifique com verdade.** Preço = materiais + seu tempo + custos fixos
    + margem. Cobrar "baratinho para começar" é o erro nº 1: você trabalha
    muito, sobra pouco e não sobra para reinvestir.

    **Venda onde o cliente já está.** Marketplace (como o do Magalu) dá
    alcance nacional sem custo de loja; Instagram e WhatsApp mantêm o
    relacionamento. Comece com um canal e faça bem feito.
    """
)

st.info(
    "💜 **Você não está sozinha:** o Sebrae tem trilhas gratuitas para "
    "mulheres empreendedoras (Sebrae Delas), e o crédito orientado do "
    "microempreendedor costuma ter condições especiais para MEI formalizada."
)
