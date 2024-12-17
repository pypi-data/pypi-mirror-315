# streamlit-theme-provider

Streamlit component that allows you to get the current theme.

## Installation instructions

```sh
pip install streamlit-theme-provider
```

## Usage instructions

value will be a dictionary containing the current theme settings.

```python
import streamlit as st

from streamlit_theme_provider import streamlit_theme_provider

value = streamlit_theme_provider()

st.write(value)
