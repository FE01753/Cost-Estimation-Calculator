import streamlit as st

# 頁面基本設定
st.set_page_config(page_title="E&M Quotation Cost Estimation", page_icon="⚡", layout="centered")

st.title("⚡ E&M Quotation Cost Estimation Calculator")
st.markdown("請輸入合約總價及各項成本，系統將會實時計算保險、總成本及預估利潤。")
st.markdown("---")

# 1. Quotation Sum (A)
st.subheader("1. 報價總額 (Quotation Sum A)")
quotation_sum = st.number_input("Quotation Sum (A) [HKD]", value=560000.0, step=1000.0, format="%.2f")

# 2. Category 1: MA (Material / Maintenance)
st.subheader("2. Category: 1.MA (物料/內部成本)")
col_ma1, col_ma2 = st.columns(2)
with col_ma1:
    ma_m190 = st.number_input("(M190) Specialist Material", value=2800.0, step=100.0, format="%.2f")
    # 其他 MA 項目預設為 0，可按需擴充
    ma_others = 0.0 
total_ma = ma_m190 + ma_others
st.text(f"Total Cost for Category: 1.MA = ${total_ma:,.2f}")

# 3. Category 2: SC (Sub-contractor)
st.subheader("3. Category: 2.SC (分判商)")
col_sc1, col_sc2 = st.columns(2)
with col_sc1:
    sc_m210 = st.number_input("(M210) HVAC Sub-contractor", value=480000.0, step=1000.0, format="%.2f")
    sc_others = 0.0
total_sc = sc_m210 + sc_others
st.text(f"Total Cost for Category: 2.SC = ${total_sc:,.2f}")

# 4. Direct Expenses & Labour
st.subheader("4. 人工與直接開支")
col_exp1, col_exp2 = st.columns(2)
with col_exp1:
    labour_wages = st.number_input("3. Labour and wages", value=12000.0, step=500.0, format="%.2f")
    ot_allowance = st.number_input("4. OT and allowance", value=0.0, step=500.0, format="%.2f")
with col_exp2:
    transportation = st.number_input("5. Transportation", value=0.0, step=100.0, format="%.2f")
    other_expenses = st.number_input("6. Other direct expenses", value=0.0, step=100.0, format="%.2f")

# 5. Insurance (自動依公式計算)
st.subheader("7. Insurance (保險費)")
col_ins1, col_ins2, col_ins3 = st.columns(3)
with col_ins1:
    ec_pct = st.number_input("(EC) %", value=1.25, step=0.01, format="%.2f")
    ec_val = quotation_sum * (ec_pct / 100.0)
    st.write(f"EC: ${ec_val:,.2f}")
with col_ins2:
    car_pct = st.number_input("(CAR) %", value=0.45, step=0.01, format="%.2f") # 已修正為 0.45%
    car_val = quotation_sum * (car_pct / 100.0)
    st.write(f"CAR: ${car_val:,.2f}")
with col_ins3:
    levy_pct = st.number_input("(Levy) EC %", value=10.80, step=0.01, format="%.2f")
    levy_val = ec_val * (levy_pct / 100.0)
    st.write(f"Levy: ${levy_val:,.2f}")

total_insurance = ec_val + car_val + levy_val

# 6. Bonus & Risk
st.subheader("8 & 9. Bonus 與風險準備金")
col_br1, col_br2 = st.columns(2)
with col_br1:
    bonus_pct = st.number_input("(BONUS) Wages %", value=10.0, step=0.1, format="%.2f")
    bonus_val = labour_wages * (bonus_pct / 100.0)
    st.write(f"Bonus: ${bonus_val:,.2f}")
with col_br2:
    risk_pct = st.number_input("9. MA & SC Risk [M199] %", value=1.0, step=0.1, format="%.2f")
    risk_val = quotation_sum * (risk_pct / 100.0)
    st.write(f"Risk: ${risk_val:,.2f}")

# --- 總結計算 (Summary) ---
total_cost_b = total_ma + total_sc + labour_wages + ot_allowance + transportation + other_expenses + total_insurance + bonus_val + risk_val
estimated_profits_c = quotation_sum - total_cost_b
profit_percentage = (estimated_profits_c / quotation_sum * 100.0) if quotation_sum > 0 else 0.0

st.markdown("---")
st.subheader("📊 最終利潤結算 (Summary)")

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="Total Cost (B)", value=f"${total_cost_b:,.2f}")
with col_res2:
    st.metric(label="Estimated Profits (C)", value=f"${estimated_profits_c:,.2f}")
with col_res3:
    st.metric(label="Profit Percentage", value=f"{profit_percentage:.2f}%")
