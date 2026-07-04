# -*- coding: utf-8 -*-
"""Ceuc_IA · Evidência — por que este projeto existe.
Séries anuais da PNAD Contínua (IBGE/SIDRA, tabela 4093) + a fotografia
das mães que saem do mercado (IBGE Estatísticas de Gênero e estudo FGV)."""

import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from utils.branding import aplicar_marca

VERDE_ESCURO = "#0F6E56"
VERDE_MEDIO = "#1D9E75"
VERDE_PASTEL = "#DFF2E9"
CINZA = "#888780"
LARANJA = "#D85A30"

st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #FBFDFC; }}
      [data-testid="stMetric"] {{
          background-color: {VERDE_PASTEL};
          border-radius: 12px; padding: 14px 18px;
      }}
      h1, h2, h3 {{ color: {VERDE_ESCURO}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

aplicar_marca()

UFS = {
    "Brasil": ("n1", "all"),
    "Rondônia": ("n3", "11"), "Acre": ("n3", "12"), "Amazonas": ("n3", "13"),
    "Roraima": ("n3", "14"), "Pará": ("n3", "15"), "Amapá": ("n3", "16"),
    "Tocantins": ("n3", "17"), "Maranhão": ("n3", "21"), "Piauí": ("n3", "22"),
    "Ceará": ("n3", "23"), "Rio Grande do Norte": ("n3", "24"),
    "Paraíba": ("n3", "25"), "Pernambuco": ("n3", "26"), "Alagoas": ("n3", "27"),
    "Sergipe": ("n3", "28"), "Bahia": ("n3", "29"), "Minas Gerais": ("n3", "31"),
    "Espírito Santo": ("n3", "32"), "Rio de Janeiro": ("n3", "33"),
    "São Paulo": ("n3", "35"), "Paraná": ("n3", "41"),
    "Santa Catarina": ("n3", "42"), "Rio Grande do Sul": ("n3", "43"),
    "Mato Grosso do Sul": ("n3", "50"), "Mato Grosso": ("n3", "51"),
    "Goiás": ("n3", "52"), "Distrito Federal": ("n3", "53"),
}

INDICADORES = {
    "Taxa de desocupação": "Desocupação (%)",
    "Taxa de participação": "Participação na força de trabalho (%)",
    "Taxa de informalidade": "Informalidade (%)",
}
ANO_INICIAL = 2019
ANO_FINAL = 2025   # 2026 fica fora: só há 1 trimestre divulgado
N_TRIMESTRES = 32


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def buscar_sidra(nivel: str, codigo: str) -> pd.DataFrame:
    """Coleta trimestral da tabela 4093 e agrega em média anual."""
    url = (
        "https://apisidra.ibge.gov.br/values"
        f"/t/4093/{nivel}/{codigo}/v/allxp/p/last%20{N_TRIMESTRES}/c2/all"
        "?formato=json"
    )
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    dados = resp.json()
    if not dados or len(dados) < 2:
        return pd.DataFrame()

    header = dados[0]
    col_variavel = next(k for k, v in header.items() if v == "Variável")
    col_sexo = next(k for k, v in header.items() if v == "Sexo")
    col_trim_cod = next(k for k, v in header.items()
                        if "Trimestre" in v and "Código" in v)

    df = pd.DataFrame(dados[1:]).rename(columns={
        "V": "valor", col_variavel: "variavel", col_sexo: "sexo",
        col_trim_cod: "trim_cod",
    })[["variavel", "sexo", "trim_cod", "valor"]]

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["ano"] = df["trim_cod"].str[:4].astype(int)
    df = df[(df["ano"] >= ANO_INICIAL) & (df["ano"] <= ANO_FINAL)]
    df = df.dropna(subset=["valor"])

    def classifica(nome: str):
        if "Coeficiente" in nome:
            return None
        for chave, rotulo in INDICADORES.items():
            if nome.startswith(chave):
                return rotulo
        return None

    df["indicador"] = df["variavel"].map(classifica)
    df = df.dropna(subset=["indicador"])

    # Média anual dos trimestres
    anual = (df.groupby(["indicador", "sexo", "ano"], as_index=False)
               ["valor"].mean())
    return anual.sort_values("ano").reset_index(drop=True)


def serie(df, indicador, sexo):
    return df[(df["indicador"] == indicador) & (df["sexo"] == sexo)]


def grafico_mh(df, indicador, titulo):
    fig = go.Figure()
    estilos = {
        "Mulheres": dict(color=VERDE_ESCURO, width=3),
        "Homens": dict(color=CINZA, width=2, dash="dot"),
    }
    for sexo, linha in estilos.items():
        s = serie(df, indicador, sexo)
        fig.add_trace(go.Scatter(
            x=s["ano"], y=s["valor"], name=sexo,
            mode="lines+markers", line=linha,
            hovertemplate="%{x}<br>%{y:.1f}%<extra>" + sexo + "</extra>",
        ))
    fig.update_layout(
        title=titulo, template="plotly_white", height=380,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.12),
        yaxis_ticksuffix="%", xaxis=dict(dtick=1),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


st.image("assets/logo.png", width=280)
st.title("📊 Evidência — por que o Ceuc_IA existe")
st.caption(
    "Médias anuais da PNAD Contínua (IBGE, tabela SIDRA 4093), de "
    f"{ANO_INICIAL} a {ANO_FINAL}, coletadas em tempo real da API. "
    "2026 fica fora do estudo por ter apenas um trimestre divulgado."
)

territorio = st.selectbox("Território", list(UFS.keys()), index=0)
nivel, codigo = UFS[territorio]

with st.spinner(f"Consultando a API do SIDRA para {territorio}..."):
    try:
        df = buscar_sidra(nivel, codigo)
    except Exception as exc:
        st.error(f"Não foi possível consultar a API do SIDRA agora. ({exc})")
        st.stop()

if df.empty:
    st.warning("A API não retornou dados para esse território.")
    st.stop()

ultimo_ano = int(df["ano"].max())
rotulos = list(INDICADORES.values())


def kpi(indicador):
    m = serie(df, indicador, "Mulheres")["valor"]
    h = serie(df, indicador, "Homens")["valor"]
    if m.empty or h.empty:
        return None
    return m.iloc[-1], h.iloc[-1], m.iloc[-1] - h.iloc[-1]


st.markdown(f"**Médias de {ultimo_ano}** (mulheres, com o gap vs homens):")
c1, c2, c3 = st.columns(3)
for col, ind in zip((c1, c2, c3), rotulos):
    res = kpi(ind)
    with col:
        if res is None:
            st.metric(ind, "—")
        else:
            m, h, gap = res
            st.metric(
                ind, f"{m:.1f}%",
                delta=f"{gap:+.1f} p.p. vs homens",
                delta_color="inverse" if "Participação" not in ind
                else "normal",
            )

st.divider()
g1, g2 = st.columns(2)
with g1:
    st.plotly_chart(grafico_mh(df, rotulos[0],
                    "Desocupação — média anual"),
                    use_container_width=True)
with g2:
    st.plotly_chart(grafico_mh(df, rotulos[1],
                    "Participação na força de trabalho"),
                    use_container_width=True)
st.plotly_chart(grafico_mh(df, rotulos[2],
                "Informalidade entre pessoas ocupadas"),
                use_container_width=True)

part_m = serie(df, rotulos[1], "Mulheres")[["ano", "valor"]]
part_h = serie(df, rotulos[1], "Homens")[["ano", "valor"]]
if not part_m.empty and not part_h.empty:
    gap_df = part_m.merge(part_h, on="ano", suffixes=("_m", "_h"))
    gap_df["gap"] = gap_df["valor_h"] - gap_df["valor_m"]
    fig_gap = go.Figure(go.Bar(
        x=gap_df["ano"], y=gap_df["gap"], marker_color=LARANJA,
        hovertemplate="%{x}<br>gap: %{y:.1f} p.p.<extra></extra>",
    ))
    fig_gap.update_layout(
        title="O dado que dói: gap de participação (homens − mulheres)",
        template="plotly_white", height=340,
        margin=dict(l=10, r=10, t=50, b=10),
        yaxis_title="pontos percentuais", xaxis=dict(dtick=1),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gap, use_container_width=True)

# =====================================================================
# A FOTOGRAFIA DAS MÃES — quem sai do mercado quando os filhos chegam
# =====================================================================
st.header("👶 O momento em que elas saem: a fotografia das mães")
st.markdown(
    "Os agregados acima mostram o gap entre mulheres e homens. Mas o corte "
    "que revela a **penalidade da maternidade** é outro: comparar quem vive "
    "com crianças pequenas e quem não vive. Os dados abaixo vêm de estudos "
    "nacionais de referência."
)

# --- 1) Trajetória de emprego após a licença-maternidade (FGV) --------
# Fonte: Machado & Pinho Neto (FGV EPGE), "Licença-maternidade e suas
# consequências no mercado de trabalho do Brasil" — 247,5 mil mulheres
# (25-35 anos) que tiraram licença entre 2009-2012, dados RAIS/MTE.
# Pontos-chave relatados: desligamentos de 5% no 5º mês e 15% no 6º
# (fim da estabilidade); ~48-50% fora do mercado após 12-24 meses;
# padrão persiste aos 47 meses. Curva abaixo: reconstrução aproximada.
fgv = pd.DataFrame({
    "mes": [0, 4, 5, 6, 9, 12, 24, 47],
    "empregadas": [100, 100, 95, 80, 62, 52, 50, 50],
})
fig_fgv = go.Figure()
fig_fgv.add_trace(go.Scatter(
    x=fgv["mes"], y=fgv["empregadas"], mode="lines+markers",
    line=dict(color=LARANJA, width=4), fill="tozeroy",
    fillcolor="rgba(216,90,48,0.12)",
    hovertemplate="mês %{x}: %{y}% empregadas<extra></extra>",
    name="",
))
fig_fgv.add_vline(x=5, line_dash="dot", line_color=CINZA)
fig_fgv.add_annotation(
    x=5, y=104, text="fim da estabilidade legal", showarrow=False,
    font=dict(size=12, color=CINZA),
)
fig_fgv.add_annotation(
    x=24, y=50, text="metade fora do mercado", showarrow=True,
    arrowhead=2, ax=0, ay=-40, font=dict(color=LARANJA),
)
fig_fgv.update_layout(
    title="Após a licença-maternidade: % de mulheres que seguem empregadas",
    template="plotly_white", height=400, showlegend=False,
    xaxis_title="meses após o início da licença",
    yaxis=dict(range=[0, 112], ticksuffix="%"),
    margin=dict(l=10, r=10, t=60, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_fgv, use_container_width=True)
st.caption(
    "Curva aproximada a partir dos resultados de Machado & Pinho Neto "
    "(FGV EPGE): 247,5 mil mulheres de 25 a 35 anos, licenças de 2009-2012, "
    "dados do Ministério do Trabalho. O pico de desligamentos ocorre no 6º "
    "mês — logo após o fim da estabilidade — e a maior parte parte do "
    "empregador, sem justa causa."
)

# --- 2) Nível de ocupação: com e sem crianças de até 3 anos (IBGE) ----
# Fonte: IBGE, Estatísticas de Gênero (PNAD Contínua 2019) —
# pessoas de 25 a 49 anos, por presença de criança de até 3 anos.
ocup = pd.DataFrame({
    "grupo": ["Com criança de até 3 anos", "Sem criança de até 3 anos"],
    "Mulheres": [54.6, 67.2],
    "Homens": [89.2, 83.4],
})
fig_ocup = go.Figure()
fig_ocup.add_trace(go.Bar(
    x=ocup["grupo"], y=ocup["Mulheres"], name="Mulheres",
    marker_color=VERDE_ESCURO, text=ocup["Mulheres"],
    texttemplate="%{text}%", textposition="outside",
))
fig_ocup.add_trace(go.Bar(
    x=ocup["grupo"], y=ocup["Homens"], name="Homens",
    marker_color=CINZA, text=ocup["Homens"],
    texttemplate="%{text}%", textposition="outside",
))
fig_ocup.update_layout(
    title="Filhos pequenos derrubam a ocupação delas — e elevam a deles",
    template="plotly_white", barmode="group", height=420,
    yaxis=dict(range=[0, 100], ticksuffix="%",
               title="nível de ocupação (25 a 49 anos)"),
    legend=dict(orientation="h", y=1.12),
    margin=dict(l=10, r=10, t=60, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_ocup, use_container_width=True)
st.caption(
    "Fonte: IBGE, Estatísticas de Gênero — PNAD Contínua 2019. A presença "
    "de uma criança de até 3 anos reduz a ocupação das mulheres em 12,6 "
    "p.p. e **aumenta** a dos homens em 5,8 p.p.: o cuidado recai sobre "
    "elas, e a carreira segue para eles."
)

# --- 3) Recorte racial + horas de cuidado (IBGE) ----------------------
col_a, col_b = st.columns(2)

with col_a:
    raca = pd.DataFrame({
        "grupo": ["Mulheres brancas", "Mulheres pretas ou pardas"],
        "valor": [62.6, 49.7],
    })
    fig_raca = go.Figure(go.Bar(
        x=raca["grupo"], y=raca["valor"],
        marker_color=[VERDE_MEDIO, LARANJA],
        text=raca["valor"], texttemplate="%{text}%",
        textposition="outside",
    ))
    fig_raca.update_layout(
        title="Mães com criança de até 3 anos:<br>a desigualdade tem cor",
        template="plotly_white", height=380,
        yaxis=dict(range=[0, 80], ticksuffix="%",
                   title="nível de ocupação"),
        margin=dict(l=10, r=10, t=70, b=10), showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_raca, use_container_width=True)

with col_b:
    horas = pd.DataFrame({
        "grupo": ["Mulheres", "Homens"],
        "valor": [21.4, 11.0],
    })
    fig_horas = go.Figure(go.Bar(
        x=horas["grupo"], y=horas["valor"],
        marker_color=[VERDE_ESCURO, CINZA],
        text=horas["valor"], texttemplate="%{text}h",
        textposition="outside",
    ))
    fig_horas.update_layout(
        title="Horas semanais dedicadas a cuidados<br>e afazeres domésticos",
        template="plotly_white", height=380,
        yaxis=dict(range=[0, 28], title="horas por semana"),
        margin=dict(l=10, r=10, t=70, b=10), showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_horas, use_container_width=True)

st.caption(
    "Fonte: IBGE, Estatísticas de Gênero — PNAD Contínua 2019. As mulheres "
    "dedicam quase o dobro das horas dos homens ao trabalho de cuidado não "
    "remunerado — a 'segunda jornada' que espreme o tempo disponível para "
    "o mercado."
)

st.success(
    "**É essa a barreira que o Ceuc_IA ataca:** a saída forçada após a "
    "licença, a sobrecarga de cuidado e a falta de pontes de volta. A IA "
    "identifica o caminho viável para cada mãe — vaga compatível com a "
    "rotina ou empreendedorismo formalizado — antes que a saída se torne "
    "permanente."
)

with st.expander("⚠️ Nota metodológica"):
    st.markdown(
        """
        - As séries anuais (topo da página) são **médias dos trimestres** da
          PNAD Contínua, tabela SIDRA 4093, consultadas em tempo real.
          **2026 está fora do estudo** por ter apenas 1 trimestre divulgado.
        - Os agregados do SIDRA abrem por sexo, não por maternidade. Os
          gráficos desta seção usam o recorte por **presença de crianças no
          domicílio** (IBGE, Estatísticas de Gênero) e a trajetória
          pós-licença do estudo da FGV (curva aproximada dos resultados
          publicados).
        - No roadmap do Ceuc_IA, esses recortes passam a ser calculados
          direto dos **microdados** da PNAD Contínua no pipeline Medallion
          (Magalu Cloud), com atualização contínua e abertura por UF.
        """
    )

st.caption("Ceuc_IA · Fontes: IBGE (SIDRA 4093 e "
           "Estatísticas de Gênero 2019) e FGV EPGE (Machado & Pinho Neto).")
