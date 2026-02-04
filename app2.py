import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 頁面設定
st.set_page_config(page_title="萌萌個案小管家", page_icon="🐾", layout="wide")

# 自定義可愛 CSS
st.markdown("""
    <style>
    .stApp { background-color: #fffaf0; }
    .stButton>button { border-radius: 20px; border: 2px solid #ffb6c1; background-color: #fff; color: #ff69b4; }
    h1 { color: #ff69b4; }
    .reminder-card { background-color: #ffe4e1; padding: 15px; border-radius: 15px; border-left: 5px solid #ff69b4; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐾 萌萌個案小管家")

# 2. 初始化資料庫
if 'case_db' not in st.session_state:
    st.session_state.case_db = pd.DataFrame(columns=[
        "案號", "名字", "風險", "主要物質", "個案來源", "治療醫院", "服務區間_起", "服務區間_迄", "家訪區間_起", "家訪區間_迄"
    ])

# 3. 🔔 溫馨提醒邏輯 (最上方顯示)
st.subheader("🔔 待辦小提醒")
today = datetime.today().date()
reminders = []

if not st.session_state.case_db.empty:
    for _, row in st.session_state.case_db.iterrows():
        # 檢查家訪區間是否快到了 (3天內)
        visit_start = row["家訪區間_起"]
        if 0 <= (visit_start - today).days <= 3:
            reminders.append(f"🏠 **{row['名字']}** 的家訪時間快到囉！({visit_start})")
        
        # 檢查服務區間是否快結束了 (7天內)
        service_end = row["服務區間_迄"]
        if 0 <= (service_end - today).days <= 7:
            reminders.append(f"🎈 **{row['名字']}** 的服務區間即將結束！({service_end})")

if reminders:
    for r in reminders:
        st.markdown(f'<div class="reminder-card">{r}</div>', unsafe_allow_html=True)
else:
    st.write("✨ 目前沒有急事，可以喝口水休息一下喔！")

st.divider()

# 4. 選單定義與分頁
risk_levels = ["💖 低風險", "💛 中風險", "🔥 高風險"]
substances = ["🍬 依托咪酯", "💉 海洛因", "⚡ 安非他命", "🌿 大麻", "🌀 愷他命", "🌈 多重藥物", "❓ 其他"]
sources = ["⚖️ 緩起訴", "🔓 服刑期滿", "🕊️ 假釋期滿", "⚠️ 三四級毒品", "🏫 教育局轉介", "🏢 地檢署轉介", "🤝 貫穿式", "🙋 自行求助"]
hospitals = ["🏥 聯醫板橋", "🏥 八療土城", "🏥 亞東醫院", "🏥 聯醫三重", "🎉 完成治療", "✅ 無需治療", "🏘️ 社區處遇", "🌻 利伯他茲", "➕ 自行新增"]

tab1, tab2 = st.tabs(["🌸 新增小個案", "📂 個案大本營"])

with tab1:
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            custom_id = st.text_input("⭐ 個案編號")
            name = st.text_input("🧸 怎麼稱呼")
            risk = st.selectbox("🚩 風險評估", risk_levels)
        with col2:
            substance = st.selectbox("🍬 主要物質", substances)
            source = st.selectbox("📍 個案來源", sources)
            hospital = st.selectbox("🏥 醫院/狀態", hospitals)
            
        st.write("📅 **區間設定**")
        c3, c4 = st.columns(2)
        with c3:
            s_range = st.date_input("🎈 服務區間", value=[today, today + timedelta(days=30)])
        with c4:
            v_range = st.date_input("🏠 家訪預計區間", value=[today + timedelta(days=7), today + timedelta(days=10)])
            
        if st.form_submit_button("✨ 紀錄儲存 ✨"):
            if custom_id and name:
                new_data = {
                    "案號": custom_id, "名字": name, "風險": risk,
                    "主要物質": substance, "個案來源": source, "治療醫院": hospital,
                    "服務區間_起": s_range[0], "服務區間_迄": s_range[1],
                    "家訪區間_起": v_range[0], "家訪區間_迄": v_range[1]
                }
                st.session_state.case_db = pd.concat([st.session_state.case_db, pd.DataFrame([new_data])], ignore_index=True)
                st.success(f"🎊 {name} 存好囉！")
                st.balloons()
                st.rerun()

with tab2:
    if st.session_state.case_db.empty:
        st.write("清單空空的 🐾")
    else:
        # 整理顯示用的資料表（合併區間成字串）
        display_df = st.session_state.case_db.copy()
        display_df["服務區間"] = display_df["服務區間_起"].astype(str) + " ~ " + display_df["服務區間_迄"].astype(str)
        display_df["家訪區間"] = display_df["家訪區間_起"].astype(str) + " ~ " + display_df["家訪區間_迄"].astype(str)
        
        st.dataframe(display_df[["案號", "名字", "風險", "主要物質", "個案來源", "治療醫院", "服務區間", "家訪區間"]], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("🗑️ 整理個案")
        delete_options = st.session_state.case_db.apply(lambda x: f"{x['案號']} - {x['名字']}", axis=1).tolist()
        target = st.selectbox("要移除哪位個案？", ["請選擇"] + delete_options)
        if st.button("確認刪除"):
            if target != "請選擇":
                tid = target.split(" - ")[0]
                st.session_state.case_db = st.session_state.case_db[st.session_state.case_db["案號"] != tid]
                st.rerun()
