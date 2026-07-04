# -*- coding: utf-8 -*-
"""Dados mocados do MVP.
Em produção, as vagas vêm do PostgreSQL gerenciado (alimentado por
integrações com ATSs parceiros) e a trilha de empreendedorismo é servida
via RAG na VM GPU."""

EMPRESAS = [
    {
        "empresa": "Lojas Aurora",
        "vaga": "Assistente administrativo",
        "setor": "Varejo",
        "modalidade": "Híbrido",
        "horario": "Meio período",
        "beneficios": ["Auxílio creche", "Banco de horas", "VT/VR"],
        "habilidades": ["Organização", "Excel / planilhas",
                        "Atendimento ao cliente"],
        "cidade": "Recife/PE",
    },
    {
        "empresa": "TechNorde",
        "vaga": "Analista de suporte júnior",
        "setor": "Tecnologia",
        "modalidade": "Remoto",
        "horario": "Horários flexíveis",
        "beneficios": ["Home office", "Horário flexível", "Plano de saúde"],
        "habilidades": ["Informática", "Atendimento ao cliente",
                        "Escrita e comunicação"],
        "cidade": "Remoto (Brasil)",
    },
    {
        "empresa": "Grupo Educar+",
        "vaga": "Auxiliar de sala (educação infantil)",
        "setor": "Educação",
        "modalidade": "Presencial",
        "horario": "Meio período",
        "beneficios": ["Auxílio creche", "Bolsa de estudos para filhos"],
        "habilidades": ["Cuidado infantil", "Organização", "Criatividade"],
        "cidade": "Recife/PE",
    },
    {
        "empresa": "FinanBrasil",
        "vaga": "Assistente financeiro",
        "setor": "Financeiro",
        "modalidade": "Híbrido",
        "horario": "Período integral",
        "beneficios": ["Auxílio creche", "PLR", "Plano de carreira"],
        "habilidades": ["Excel / planilhas", "Organização",
                        "Escrita e comunicação"],
        "cidade": "Recife/PE",
    },
    {
        "empresa": "Contact Nordeste",
        "vaga": "Atendente de relacionamento",
        "setor": "Serviços",
        "modalidade": "Remoto",
        "horario": "Meio período",
        "beneficios": ["Home office", "Escala flexível"],
        "habilidades": ["Atendimento ao cliente", "Escrita e comunicação",
                        "Negociação"],
        "cidade": "Remoto (Brasil)",
    },
    {
        "empresa": "Rede Bem Viver",
        "vaga": "Recepcionista de clínica",
        "setor": "Saúde",
        "modalidade": "Presencial",
        "horario": "Período integral",
        "beneficios": ["Plano de saúde", "VT/VR"],
        "habilidades": ["Atendimento ao cliente", "Organização",
                        "Informática"],
        "cidade": "Olinda/PE",
    },
    {
        "empresa": "Criativa Marketing",
        "vaga": "Social media júnior",
        "setor": "Comunicação",
        "modalidade": "Remoto",
        "horario": "Horários flexíveis",
        "beneficios": ["Home office", "Horário flexível"],
        "habilidades": ["Redes sociais", "Criatividade",
                        "Escrita e comunicação"],
        "cidade": "Remoto (Brasil)",
    },
]

# Sugestão de negócio por habilidade dominante
NEGOCIOS_POR_HABILIDADE = {
    "Culinária": {
        "negocio": "Alimentação artesanal (marmitas, doces, salgados)",
        "cnae_exemplo": "5620-1/04 — Fornecimento de alimentos preparados",
        "canal": "Encomendas por WhatsApp/Instagram e apps de delivery",
    },
    "Artesanato": {
        "negocio": "Produtos artesanais e personalizados",
        "cnae_exemplo": "3299-0/99 — Fabricação de produtos diversos",
        "canal": "Marketplace (Magalu, Elo7) e feiras locais",
    },
    "Beleza e estética": {
        "negocio": "Serviços de beleza em domicílio ou estúdio",
        "cnae_exemplo": "9602-5/02 — Atividades de estética",
        "canal": "Agenda por Instagram e indicação de clientes",
    },
    "Costura": {
        "negocio": "Ateliê de costura, ajustes e sob medida",
        "cnae_exemplo": "9529-1/99 — Reparação de artigos pessoais",
        "canal": "Bairro + redes sociais + parcerias com lojas",
    },
    "Redes sociais": {
        "negocio": "Gestão de redes sociais para pequenos negócios",
        "cnae_exemplo": "7319-0/03 — Marketing direto",
        "canal": "Prospecção de comércios locais e boca a boca",
    },
    "Cuidado infantil": {
        "negocio": "Recreação infantil e apoio escolar",
        "cnae_exemplo": "8891-4/00 — Educação infantil (verificar exigências)",
        "canal": "Grupos de mães da região e escolas parceiras",
    },
    "Excel / planilhas": {
        "negocio": "Serviços administrativos para pequenas empresas",
        "cnae_exemplo": "8219-9/99 — Apoio administrativo",
        "canal": "Comércios do bairro e contadores parceiros",
    },
}

NEGOCIO_PADRAO = {
    "negocio": "Revenda de produtos (moda, cosméticos, utilidades)",
    "cnae_exemplo": "4781-4/00 — Comércio varejista de vestuário",
    "canal": "Marketplace (Magalu) e redes sociais",
}

PASSOS_MEI = [
    ("Criar conta gov.br", "Nível prata ou ouro, gratuita, pelo app gov.br."),
    ("Acessar o Portal do Empreendedor", "gov.br/mei → 'Quero ser MEI' → "
     "'Formalize-se'. O processo é gratuito — desconfie de sites que cobram."),
    ("Escolher as atividades (CNAE)", "Até 1 atividade principal e 15 "
     "secundárias, entre as ocupações permitidas ao MEI."),
    ("Emitir o CNPJ na hora", "O certificado (CCMEI) sai no fim do cadastro, "
     "já com CNPJ ativo."),
    ("Pagar o DAS mensal", "Guia única (~R$ 70-80, INSS + imposto) com "
     "vencimento dia 20. Garante aposentadoria, auxílio-doença e "
     "salário-maternidade."),
    ("Declarar uma vez por ano", "DASN-SIMEI, até 31 de maio, informando o "
     "faturamento do ano anterior."),
]


# Capacitação gratuita por área-alvo (trilha de transição)
CURSOS_POR_AREA = {
    "Tecnologia e dados": [
        "Ateliê Digital do Google — fundamentos com certificado gratuito",
        "DIO e Oracle ONE — bootcamps gratuitos de programação",
        "Reprograma / PrograMaria — formações em tecnologia para mulheres",
    ],
    "Administrativo e financeiro": [
        "Escola Virtual Fundação Bradesco — Excel, rotinas administrativas",
        "Sebrae EAD — finanças e gestão para o dia a dia",
        "Escola Virtual de Governo (EV.G) — cursos gratuitos com certificado",
    ],
    "Vendas e marketing digital": [
        "Ateliê Digital do Google — marketing digital com certificado",
        "RD University — inbound e vendas digitais (gratuitos)",
        "Sebrae EAD — vendas pelo WhatsApp e redes sociais",
    ],
    "Cuidado, saúde e bem-estar": [
        "SENAC EAD — cursos livres na área de saúde e bem-estar",
        "Programas estaduais gratuitos de qualificação técnica",
        "Cruz Vermelha / SUS — capacitações de cuidador e primeiros socorros",
    ],
    "Educação e social": [
        "AVAMEC (MEC) — formações gratuitas em educação",
        "Coursera com auxílio financeiro — didática e tecnologias educacionais",
        "Sebrae EAD — gestão para projetos sociais e educacionais",
    ],
}
