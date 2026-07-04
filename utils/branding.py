# -*- coding: utf-8 -*-
"""Identidade visual do Ceuc_IA (equipe Ceuc_IA)."""

from pathlib import Path
import streamlit as st

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def aplicar_marca():
    """Logo no topo da sidebar + assinatura da equipe.
    Guardado em try/except para compatibilidade com versões antigas
    do Streamlit (st.logo existe a partir da 1.35)."""
    try:
        st.logo(
            str(ASSETS / "logo.png"),
            icon_image=str(ASSETS / "logo_icone.png"),
        )
    except Exception:
        pass
    with st.sidebar:
        st.caption("**Ceuc_IA** · IA para mães no mercado de trabalho")
