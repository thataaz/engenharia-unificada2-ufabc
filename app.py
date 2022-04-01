import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os

from multiapp import MultiApp
from apps import download, datavis, stats
# app = MultiApp()
#%% Add all your application here
# app.add_app("Dashboard", datavis.app)
# app.add_app("Estatísticas", stats.app)
# app.add_app("Download", download.app)
#%% The main app
# app.run('Dashboard\nMonitoramento de Qualidade do Ar')

apps = [
    {"func": datavis.app, "title": "Dashboard", "icon": "window-split"},
    {"func": stats.app, "title": "Estatísticas", "icon": "file-bar-graph"},
    {"func": download.app, "title": "Download", "icon": "cloud-download"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0
    
with st.sidebar:
    selected = option_menu(
        "Menu Principal",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("Sobre")
    st.sidebar.info(
        """
        Dashboard do projeto de Sistema de monitoramento da Qualidade do Ar da disciplina de Engenharia Unificada II da Universidade Federal do ABC do Quadrimestre 2022.1
        
        Source code: <https://github.com/thataaz/engenharia-unificada2-ufabc>
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break