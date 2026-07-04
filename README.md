# Ceuc_IA — MVP (hackathon Magalu Cloud)

Jornada: login → questionário → IA classifica o perfil (CLT, Empreendedora
ou Transição de carreira) → vagas com matching, trilha MEI ou trilha de
reposicionamento em 5 fases.

## Rodar localmente (cmd, não PowerShell)

```
cd projeto_maes   # (renomeie a pasta para ceuc_ia se preferir)
python -m venv .venv
.venv\Scripts\activate.bat
pip install streamlit requests pandas plotly
streamlit run Ceuc_IA.py
```

## Contas de demonstração

| e-mail            | senha |
|-------------------|-------|
| maria@demo.com    | 1234  |
| ana@demo.com      | 1234  |
| juliana@demo.com  | 1234  |

## IA (opcional na demo)

A classificação tenta um LLM em endpoint OpenAI-compatible e, se ele não
responder, usa um fallback heurístico (a demo nunca quebra).

- Local (Ollama):  `ollama run llama3.1` — o app usa
  `http://localhost:11434/v1` por padrão.
- Magalu Cloud (vLLM na VM GPU): defina as variáveis de ambiente
  `LLM_ENDPOINT` (ex.: `http://10.0.1.20:8000/v1`) e `LLM_MODEL`.

## Estrutura

```
Ceuc_IA.py                 # login (dados mocados) + jornada
pages/1_📊_Evidencia.py    # dados IBGE/SIDRA anuais 2019-2025 + gráficos sobre mães (público)
pages/2_🧭_Meu_Perfil.py   # questionário + classificação por IA
pages/3_💼_Vagas.py        # matching com empresas (mock)
pages/4_🚀_Empreender.py   # trilha MEI / tipo de negócio
pages/5_🧗_Transicao.py    # trilha objetiva de transição de carreira
utils/auth.py              # autenticação mocada
utils/ia.py                # LLM + fallback heurístico
utils/dados.py             # vagas e trilhas mocadas
```

assets/                    # logomarca (logo.png, logo_icone.png, logo_fundo_branco.png)
