from pathlib import Path
import sys

import streamlit as st


sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))  # to use OpenSSA in same repo


st.title('SSA-Powered Problem Solvers')
