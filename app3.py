import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 頁面設定
st.set_page_config(page_title="萌萌個案小管家", page_icon="🐾", layout="wide")

# 加強版可愛 CSS：字體加大、標題加粗
st.markdown("""
    <style>
    /* 全域字體加大 */
    html, body, [class*="st-"] {
        font-size: 18px; 
        font-family: 'Microsoft JhengHei', sans-serif;
    }
    .stApp { background-color: #fffaf0; }
    
    /* 標題與副標題加大 */
    h1 { color: #ff69b4; font-size: 42px !important; font-weight: 800 !important; }
    h2, h3 { color: #ff1493; font-size: 30px !important; font-weight: 700 !important; }
    
    /* 提醒卡片加強 */
    .reminder-card { 
        background-color: #fff0f5; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 8px solid #ff1493; 
        margin-bottom: 15px;
        font-size: 22px !important;
        font-weight: bold;
        color: #8b008b;
    }

    /* 表單標籤加大 */
    .stWidgetLabel p {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #4b0082 !important;
    }

    /* 按鈕加大 */
    .stButton>button { 
        font-size: 22px !important;
        padding: 10px 30px !important;
        border-radius: 30px; 
        border: 3px solid #ffb6c1; 
        background-color: #fff; 
        color: #ff69b4;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🐾 萌萌個案小管家")

# 2. 初始化資料庫
if 'case_db' not in st.session_state:
    st.session_state.case_db = pd.DataFrame(columns=[
        "案號", "名字", "風險", "主要物質", "個案來源", "治療醫院", "服務區間_起", "服務區間_迄", "家訪區間_起
