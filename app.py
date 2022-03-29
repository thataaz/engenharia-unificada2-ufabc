import streamlit as st
import pandas as pd
import os

from multiapp import MultiApp
from apps import download, datavis, stats
app = MultiApp()

#%% Add all your application here
app.add_app("Dashboard", datavis.app)
app.add_app("Estatísticas", stats.app)
app.add_app("Download", download.app)

#%% The main app
app.run('Dashboard\nMonitoramento de Qualidade do Ar')