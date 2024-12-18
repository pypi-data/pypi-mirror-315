import streamlit as st

# pip install streamlit-ace
from streamlit_ace import st_ace

# Spawn a new Ace editor
content = st_ace(
    placeholder="请输入python代码",
    language="python",
    # theme="monokai",
)
print(content)

# Display editor's content as you type
st.code(content, language="python")