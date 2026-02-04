import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="藥癮個案管理系統", layout="wide")
st.title("🏥 藥癮個案管理系統")

# 2. 初始化資料庫 (若不存在則建立)
if 'case_db' not in st.session_state:
    # 建立初始空的 DataFrame
    st.session_state.case_db = pd.DataFrame(columns=[
        "個案編號", "姓名", "風險等級", "主要物質", "個案來源", "治療醫院/處遇", "服務區間", "家訪區間"
    ])

# 3. 選單定義
risk_levels = ["🔴 高風險", "🟡 中風險", "🟢 低風險"]
substances = ["依托咪酯 (Etomidate)", "海洛因", "安非他命", "愷他命 (K)", "大麻", "多重藥物", "其他"]
sources = ["法院轉介", "地檢署緩起訴", "醫療機構轉介", "自行求助", "家屬代求助"]
hospitals = ["聯醫板橋", "八療土城", "亞東醫院", "聯醫三重", "完成治療", "無需治療", "社區處遇", "利伯他茲", "自行新增"]

# 4. 功能分頁
tab1, tab2 = st.tabs(["➕ 新增個案", "📋 管理個案清單"])

# --- 分頁 1: 新增個案 ---
with tab1:
    st.subheader("請填寫個案資料")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            custom_id = st.text_input("個案編號 (請手動輸入)")
            name = st.text_input("姓名/化名")
            risk = st.selectbox("風險等級", risk_levels)
        with col2:
            substance = st.selectbox("主要物質", substances)
            source = st.selectbox("個案來源", sources)
            hospital = st.selectbox("戒癮治療醫院/處遇", hospitals)
            
        st.divider()
        st.subheader("📅 時間區間設定")
        col3, col4 = st.columns(2)
        with col3:
            service_range = st.date_input("服務區間", value=[datetime.today(), datetime.today()])
        with col4:
            visit_range = st.date_input("家訪區間", value=[datetime.today(), datetime.today()])
        
        submitted = st.form_submit_button("儲存個案資料")
        
        if submitted:
            if custom_id and name:
                # 檢查編號是否重複
                if custom_id in st.session_state.case_db["個案編號"].values:
                    st.error(f"❌ 編號 {custom_id} 已存在，請檢查後重新輸入。")
                else:
                    # 建立新資料列
                    new_data = {
                        "個案編號": custom_id,
                        "姓名": name,
                        "風險等級": risk,
                        "主要物質": substance,
                        "個案來源": source,
                        "治療醫院/處遇": hospital,
                        "服務區間": f"{service_range[0]} ~ {service_range[1]}",
                        "家訪區間": f"{visit_range[0]} ~ {visit_range[1]}"
                    }
                    # 加入儲存空間
                    st.session_state.case_db = pd.concat([st.session_state.case_db, pd.DataFrame([new_data])], ignore_index=True)
                    st.success(f"✅ 個案 {name} (編號: {custom_id}) 已新增成功！")
            else:
                st.error("❌ 「個案編號」與「姓名」為必填項目。")

# --- 分頁 2: 管理個案清單 (含刪除功能) ---
with tab2:
    st.subheader("現有個案清單")
    
    if st.session_state.case_db.empty:
        st.info("目前尚無個案資料。")
    else:
        # 顯示互動式表格
        st.dataframe(st.session_state.case_db, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("🗑️ 刪除個案")
        
        # 建立刪除選擇清單：顯示「編號 - 姓名」
        delete_options = st.session_state.case_db.apply(lambda x: f"{x['個案編號']} - {x['姓名']}", axis=1).tolist()
        target_selection = st.selectbox("選擇要刪除的個案", ["請選擇"] + delete_options)
        
        if st.button("確認刪除資料", type="primary"):
            if target_selection != "請選擇":
                # 取得編號部分
                target_id = target_selection.split(" - ")[0]
                # 過濾掉該編號
                st.session_state.case_db = st.session_state.case_db[st.session_state.case_db["個案編號"] != target_id]
                st.warning(f"⚠️ 已刪除個案：{target_selection}")
                st.rerun() # 重新整理頁面
            else:
                st.info("請先從下拉選單選擇一個個案。")
