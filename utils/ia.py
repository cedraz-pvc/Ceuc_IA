# -*- coding: utf-8 -*-
"""Classificação do perfil profissional (CLT vs Empreendedora).

Estratégia em duas camadas:
1) LLM via endpoint OpenAI-compatible — funciona igual com Ollama local
   (http://localhost:11434/v1) e com vLLM na VM GPU da Magalu Cloud.
   Configure com as variáveis de ambiente LLM_ENDPOINT e LLM_MODEL.
2) Fallback heurístico determinístico — garante que a demo nunca quebra
   se o modelo estiver fora do ar.
"""

import os
import json
import requests

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")

PROMPT_SISTEMA = """Você é uma orientadora de carreira especializada na \
reinserção de mães no mercado de trabalho brasileiro. Analise o \
questionário e classifique o perfil em "CLT" (empregada com carteira), \
"EMPREENDEDORA" (negócio próprio) ou "TRANSICAO" (quer mudar de área e \
precisa se reposicionar antes de buscar vagas). Considere: disponibilidade de horário, \
rede de apoio para os filhos, apetite a risco, desejo de autonomia, \
experiência prévia com vendas próprias e habilidades declaradas.
Responda APENAS com JSON válido, sem markdown, no formato:
{"perfil": "CLT", "EMPREENDEDORA" ou "TRANSICAO", "confianca": 0 a 100,
 "justificativa": "texto curto e acolhedor em português",
 "habilidades_destaque": ["...", "..."],
 "recomendacoes": ["...", "...", "..."]}"""


def _via_llm(respostas: dict) -> dict | None:
    try:
        r = requests.post(
            f"{LLM_ENDPOINT}/chat/completions",
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": PROMPT_SISTEMA},
                    {"role": "user",
                     "content": json.dumps(respostas, ensure_ascii=False)},
                ],
                "temperature": 0.2,
            },
            timeout=60,
        )
        r.raise_for_status()
        texto = r.json()["choices"][0]["message"]["content"]
        texto = texto.replace("```json", "").replace("```", "").strip()
        resultado = json.loads(texto)
        if resultado.get("perfil") in ("CLT", "EMPREENDEDORA", "TRANSICAO"):
            resultado["origem"] = "llm"
            return resultado
    except Exception:
        pass
    return None


HABILIDADES_EMPREENDER = {
    "Artesanato", "Culinária", "Beleza e estética", "Costura",
    "Redes sociais", "Criatividade", "Negociação",
}
HABILIDADES_CLT = {
    "Excel / planilhas", "Informática", "Escrita e comunicação",
    "Atendimento ao cliente", "Organização", "Liderança",
}


def _via_heuristica(respostas: dict) -> dict:
    # Transição de carreira tem prioridade: quem quer mudar de área
    # precisa se reposicionar antes de escolher entre CLT e negócio.
    if respostas.get("objetivo_carreira") == "Quero mudar de área":
        habilidades = list(respostas.get("habilidades", []))[:4]
        return {
            "perfil": "TRANSICAO",
            "confianca": 85,
            "justificativa": (
                "Você quer mudar de área — e isso pede um caminho próprio: "
                "antes de sair se candidatando, vamos reposicionar suas "
                "habilidades, fechar as lacunas com capacitação rápida e "
                "reconstruir sua narrativa profissional. A trilha de "
                "transição organiza tudo isso em passos objetivos."
            ),
            "habilidades_destaque": habilidades or ["Gestão do tempo",
                                                    "Resiliência"],
            "recomendacoes": [
                "Siga a trilha de Transição: uma fase por vez, sem pular",
                "Escolha UMA área-alvo — foco vale mais que amplitude",
                "Reserve 30-60 min por dia; constância vence intensidade",
            ],
            "origem": "heuristica",
        }

    pontos_emp, pontos_clt = 0, 0

    if respostas["ja_vendeu"] == "Sim":
        pontos_emp += 3
    pontos_emp += {"1": 0, "2": 0, "3": 1, "4": 2, "5": 3}[
        str(respostas["apetite_risco"])]
    pontos_emp += {"1": 0, "2": 0, "3": 1, "4": 2, "5": 3}[
        str(respostas["autonomia"])]

    if respostas["rede_apoio"] == "Sim, tenho com quem contar":
        pontos_clt += 2
    elif respostas["rede_apoio"] == "Não tenho":
        pontos_emp += 2

    if respostas["disponibilidade"] in ("Período integral", "Apenas remoto"):
        pontos_clt += 2
    elif respostas["disponibilidade"] == "Horários flexíveis / por conta":
        pontos_emp += 2

    habilidades = set(respostas["habilidades"])
    pontos_emp += len(habilidades & HABILIDADES_EMPREENDER)
    pontos_clt += len(habilidades & HABILIDADES_CLT)

    if respostas["anos_experiencia"] >= 3:
        pontos_clt += 1

    perfil = "EMPREENDEDORA" if pontos_emp > pontos_clt else "CLT"
    total = pontos_emp + pontos_clt or 1
    confianca = round(100 * max(pontos_emp, pontos_clt) / total)

    if perfil == "CLT":
        justificativa = (
            "Sua disponibilidade, rede de apoio e experiência indicam que "
            "uma vaga com carteira assinada — de preferência flexível ou "
            "remota — é o caminho mais seguro para o seu momento."
        )
        recomendacoes = [
            "Atualize seu currículo destacando as habilidades identificadas",
            "Priorize vagas com flexibilidade e apoio à parentalidade",
            "Prepare-se para entrevistas conhecendo seus direitos como mãe",
        ]
    else:
        justificativa = (
            "Seu desejo de autonomia, sua experiência com vendas e suas "
            "habilidades apontam para o empreendedorismo como caminho "
            "compatível com a sua rotina."
        )
        recomendacoes = [
            "Formalize-se como MEI para emitir notas e ter cobertura do INSS",
            "Comece vendendo em marketplaces para ganhar alcance sem loja",
            "Separe as finanças do negócio das finanças da casa desde o dia 1",
        ]

    destaque = list(habilidades)[:4] or ["Gestão do tempo", "Resiliência"]
    return {
        "perfil": perfil,
        "confianca": max(confianca, 55),
        "justificativa": justificativa,
        "habilidades_destaque": destaque,
        "recomendacoes": recomendacoes,
        "origem": "heuristica",
    }


def classificar_perfil(respostas: dict) -> dict:
    """Tenta o LLM; se indisponível, usa a heurística."""
    return _via_llm(respostas) or _via_heuristica(respostas)


PROMPT_RESUMO = """Você é uma especialista em recolocação profissional de \
mães no Brasil. Escreva um resumo profissional (4 a 6 linhas, primeira \
pessoa, tom confiante e verdadeiro) para currículo e LinkedIn. Traduza o \
período dedicado à maternidade em competências (gestão de tempo, \
priorização, resiliência, negociação) SEM esconder que existiu, e conecte \
as habilidades declaradas à área-alvo. Responda apenas com o texto do \
resumo, sem títulos."""


def gerar_resumo(respostas: dict, area_alvo: str) -> str:
    """Resumo profissional via LLM, com fallback de template."""
    try:
        r = requests.post(
            f"{LLM_ENDPOINT}/chat/completions",
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": PROMPT_RESUMO},
                    {"role": "user", "content": json.dumps(
                        {"respostas": respostas, "area_alvo": area_alvo},
                        ensure_ascii=False)},
                ],
                "temperature": 0.5,
            },
            timeout=60,
        )
        r.raise_for_status()
        texto = r.json()["choices"][0]["message"]["content"].strip()
        if texto:
            return texto
    except Exception:
        pass

    habs = ", ".join(list(respostas.get("habilidades", []))[:4]).lower()
    anos = respostas.get("anos_experiencia", 0)
    return (
        f"Profissional em transição para a área de {area_alvo.lower()}, "
        f"com {anos} anos de experiência e competências em {habs}. "
        "No período dedicado à maternidade, desenvolvi na prática gestão "
        "de tempo, priorização sob pressão e resiliência — habilidades que "
        "hoje aplico com método no ambiente profissional. Estou em "
        "capacitação ativa na área-alvo e busco uma oportunidade para "
        "gerar resultados desde o primeiro mês, com o comprometimento de "
        "quem sabe exatamente por que voltou."
    )
