import streamlit as st

# 1. 頁面基本設定
st.set_page_config(
    page_title="E&M Cost & Quotation Calculator", 
    page_icon="⚡", 
    layout="centered"
)

# 標題區
st.title("⚡ E&M Quotation Calculator")
st.caption("Professional Cost Estimation & Profit Tracker")
st.markdown("---")

# 2. Category: 1.MA & 2.SC 成本項目
st.subheader("📦 1 & 2. 主要成本 (MA & SC)")

col_c1, col_c2 = st.columns(2)
with col_c1:
    st.markdown("**1.MA (物料成本)**")
    ma_m190 = st.number_input("Specialist Material", value=2800.0, step=100.0, format="%.2f")
    ma_others = st.number_input("Other MA Items", value=0.0, step=100.0, format="%.2f")
    total_ma = ma_m190 + ma_others
    st.text(f"Subtotal MA: ${total_ma:,.2f}")

with col_c2:
    st.markdown("**2.SC (分判商)**")
    sc_m210 = st.number_input("Sub-contractor Cost", value=0.0, step=1000.0, format="%.2f")
    sc_others = st.number_input("Other SC Items", value=0.0, step=100.0, format="%.2f")
    total_sc = sc_m210 + sc_others
    st.text(f"Subtotal SC: ${total_sc:,.2f}")

# 3. 人工與直接開支
st.markdown("---")
st.subheader("👷‍♂️ 3. 人工與直接開支")
col_l1, col_l2 = st.columns(2)
with col_l1:
    labour_wages = st.number_input("Labour and wages", value=8800.0, step=100.0, format="%.2f")
    ot_allowance = st.number_input("OT and allowance", value=0.0, step=100.0, format="%.2f")
with col_l2:
    transportation = st.number_input("Transportation", value=0.0, step=100.0, format="%.2f")
    other_direct = st.number_input("Other direct expenses", value=0.0, step=100.0, format="%.2f")

total_labour = labour_wages + ot_allowance
base_direct_cost = total_ma + total_sc + total_labour + transportation + other_direct

# -------------------------------------------------------------
# 4. 總成本結算 & 報價調整區（放最底，先定義 Quotation Sum A）
# -------------------------------------------------------------
st.markdown("---")
st.subheader("📊 總成本與利潤結算")

quotation_sum_a = st.number_input(
    "🎯 調整報價總額 (Quotation Sum A) [HKD]", 
    value=65500.0, 
    step=1000.0, 
    format="%.2f",
    help="直接在此修改開價總額，下方利潤會即時跳動"
)

# -------------------------------------------------------------
# 5. 進階調整項目（放在結算區上方，保留摺疊，並修正對應公式）
# -------------------------------------------------------------
with st.expander("⚙️ 調整保險比例、Bonus 與風險系數 (進階設定)", expanded=False):
    
    # 比例輸入
    col_ins1, col_ins2, col_ins3 = st.columns(3)
    with col_ins1:
        ec_rate = st.number_input("(EC) %", value=1.25, step=0.01, format="%.2f") / 100.0
    with col_ins2:
        car_rate = st.number_input("(CAR) % (出街價)", value=0.45, step=0.01, format="%.2f") / 100.0
    with col_ins3:
        levy_rate = st.number_input("(Levy) EC %", value=10.80, step=0.01, format="%.2f") / 100.0
    
    col_br1, col_br2 = st.columns(2)
    with col_br1:
        bonus_pct = st.number_input("(BONUS) Wages %", value=10.0, step=0.1, format="%.2f") / 100.0
    with col_br2:
        risk_pct = st.number_input("MA & SC Risk %", value=1.0, step=0.1, format="%.2f") / 100.0

    st.markdown("---")
    st.markdown("💡 **當前百份比換算出的實際銀碼：**")
    
    # 依照 Excel 實際邏輯重新調整計算公式：
    live_ec = quotation_sum_a * ec_rate               
    live_car = quotation_sum_a * car_rate             
    live_levy = live_ec * levy_rate                   
    live_bonus = total_labour * bonus_pct             
    live_risk = quotation_sum_a * risk_pct            

    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        st.text(f"• EC 保險: ${live_ec:,.2f}")
        st.text(f"• CAR 保險: ${live_car:,.2f}")
    with r_col2:
        st.text(f"• Levy 徵費: ${live_levy:,.2f}")
        st.text(f"• Bonus 金額: ${live_bonus:,.2f}")
    with r_col3:
        st.text(f"• MA/SC 風險: ${live_risk:,.2f}")

# 正式計算用變數
ec_insurance = quotation_sum_a * ec_rate
car_insurance = quotation_sum_a * car_rate  
levy_insurance = ec_insurance * levy_rate

bonus_amount = total_labour * bonus_pct
risk_amount = quotation_sum_a * risk_pct

# 總成本 B 計算
total_cost_b = base_direct_cost + ec_insurance + car_insurance + levy_insurance + bonus_amount + risk_amount

# 最終利潤結算 C
profits_c = quotation_sum_a - total_cost_b
profit_percentage = (profits_c / quotation_sum_a * 100.0) if quotation_sum_a > 0 else 0.0

# 顯示最終計算結果面板
st.markdown("---")
res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric(label="總成本 (Total Cost B)", value=f"${total_cost_b:,.2f}")
with res_col2:
    st.metric(
        label="預估淨利潤 (Profits C)", 
        value=f"${profits_c:,.2f}", 
        delta=f"{profit_percentage:.2f}% Margin"
    )

# 智能提示
if profit_percentage < 8.0:
    st.warning("⚠️ 注意：當前預估利潤率低於公司標準範圍 (8.2% - 8.5%)，請考慮調高報價總額。")
else:
    st.success("✅ 利潤率符合目標範圍 (8.2% - 8.5% 或以上)。")

# --- 💡 低調質感水印 (Subtle & Clean Footer) ---
st.markdown("""
    <style>
    .subtle-footer {
        margin-top: 3.5rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(128, 128, 128, 0.15);
        text-align: right;
        color: rgba(128, 128, 128, 0.6);
        font-size: 0.75rem;
        letter-spacing: 0.3px;
    }
    </style>
    <div class="subtle-footer">
        Design by nikki 🤭
    </div>
""", unsafe_allow_html=True)
