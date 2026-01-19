import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

# ==========================================
# 1. 核心数据 (同步 calc.py 的 79 行数据)
# ==========================================
CSV_FILE = "prices_v3.csv"
columns = ['项目名称', '单位', 'X折叠', 'F700', '10FT', '15FT', '20FT', '30FT', '40FT']

# 完整 79 行原始数据
default_data = [
    ['无', '项', 0, 0, 0, 0, 0, 0, 0],
    ['不要', '项', 0, 0, 0, 0, 0, 0, 0],
    ['标配室内门', '樘', 0, 0, 0, 0, 0, 0, 0], 
    ['普通内墙板', '套', 0, 0, 0, 0, 0, 0, 0], 
    ['基础箱体', '台', 8000, 10000, 12000, 15000, 20000, 30000, 40000],
    ['空箱', '套', 0, 0, 0, 0, 0, 0, 0],
    ['房间数量定制', '套', 0, 0, 0, 0, 0, 0, 0],
    ['一室', '套', 500, 1000, 800, 900, 1000, 1500, 2000],
    ['两室', '套', 1000, 2000, 1500, 1800, 2000, 2500, 3000],
    ['三室', '套', 1500, 3000, 2000, 2500, 3000, 3500, 4000],
    ['四室', '套', 2000, 4000, 2500, 3000, 4000, 4500, 5000],
    ['五室', '套', 2500, 5000, 3000, 3500, 5000, 5500, 6000],
    ['六室', '套', 3000, 6000, 3500, 4000, 6000, 6500, 7000],
    ['岩棉 50mm', '平米', 0, 0, 0, 0, 0, 0, 0],
    ['岩棉 75mm', '平米', 200, 200, 200, 200, 200, 300, 400],
    ['eps 75mm', '平米', 150, 150, 150, 150, 150, 200, 300],
    ['聚氨酯 75mm', '平米', 500, 500, 500, 500, 500, 800, 1000],
    ['碳晶板(8mm)', '套', 1000, 2000, 1500, 1800, 2000, 3000, 4000],
    ['竹木纤维板', '套', 1200, 2500, 1800, 2200, 2500, 3500, 4500],
    ['普通外墙板', '套', 0, 0, 0, 0, 0, 0, 0],
    ['金属雕花板', '套', 1500, 3000, 2000, 2500, 3000, 4000, 5000],
    ['长城板', '套', 0, 2500, 2500, 2500, 2500, 3500, 4500],
    ['木芯门', '樘', 600, 600, 600, 600, 600, 600, 600],
    ['高端铝框木芯门', '樘', 800, 800, 800, 800, 800, 800, 800],
    ['谷仓门', '樘', 700, 700, 700, 700, 700, 700, 700],
    ['肯德基双开门', '樘', 2000, 2000, 2000, 2000, 2000, 2000, 2000],
    ['肯德基单开门', '樘', 1200, 1200, 1200, 1200, 1200, 1200, 1200],
    ['防盗门1', '樘', 900, 900, 900, 900, 900, 900, 900],
    ['防盗门2(钛镁合金)', '樘', 1100, 1100, 1100, 1100, 1100, 1100, 1100],
    ['断桥铝对开门', '樘', 2500, 2500, 2500, 2500, 2500, 2500, 2500],
    ['断桥铝单开门', '樘', 1500, 1500, 1500, 1500, 1500, 1500, 1500],
    ['断桥铝推拉门', '樘', 1600, 1600, 1600, 1600, 1600, 1600, 1600],
    ['钛镁合金推拉门', '樘', 1400, 1400, 1400, 1400, 1400, 1400, 1400],
    ['普通钢制对开门', '樘', 800, 800, 800, 800, 800, 800, 800],
    ['电动卷帘门', '樘', 3000, 3000, 3000, 3000, 3000, 3000, 3000],
    ['断桥铝格格单开门', '樘', 1500, 1500, 1500, 1500, 1500, 1500, 1500],
    ['钢制单开', '樘', 500, 500, 500, 500, 500, 500, 500],
    ['地板革(2mm)', '套', 300, 500, 400, 450, 600, 800, 1000],
    ['石塑锁扣地板(4cm)', '套', 600, 1000, 800, 900, 1200, 1500, 1800],
    ['断桥铝窗(不含纱窗)', '平米', 400, 400, 400, 400, 400, 400, 400],
    ['断桥铝推拉窗(含纱窗)', '平米', 450, 450, 450, 450, 450, 450, 450],
    ['铝合金推拉窗(含纱窗)', '平米', 350, 350, 350, 350, 350, 350, 350],
    ['塑钢平开窗', '平米', 300, 300, 300, 300, 300, 300, 300],
    ['塑钢推拉窗', '平米', 280, 280, 280, 280, 280, 280, 280],
    ['电动卷帘窗', '平米', 800, 800, 800, 800, 800, 800, 800],
    ['普通网', '个', 100, 100, 100, 100, 100, 100, 100],
    ['金刚网', '个', 200, 200, 200, 200, 200, 200, 200],
    ['屋顶全贴防水卷材', '项', 0, 500, 500, 500, 500, 1000, 1000],
    ['聚氨酯板75', '项', 0, 6000, 6000, 6000, 6000, 8000, 9500],
    ['聚氨酯底部保温(4cm)', '项', 0, 2500, 2500, 2500, 2500, 4000, 5000],
    ['聚氨酯底部保温(块)', '项', 0, 2000, 2000, 2000, 2000, 3000, 4000],
    ['PVC', '套', 0, 100, 100, 100, 100, 100, 100],
    ['锰铝合金', '套', 0, 200, 200, 200, 200, 200, 200],
    ['顶部瓦楞板', '套', 0, 150, 150, 150, 150, 150, 150],
    ['内顶金属雕花板', '套', 0, 200, 200, 200, 200, 200, 200],
    ['平顶', '套', 0, 100, 100, 100, 100, 100, 100],
    ['通铺屋顶', '项', 0, 4000, 5000, 5000, 5000, 7500, 10000],
    ['认证电线', '项', 1000, 1000, 1000, 1000, 1000, 2000, 2000],
    ['认证插座开关', '项', 500, 500, 500, 500, 500, 1000, 1000],
    ['认证灯', '项', 350, 350, 350, 350, 350, 600, 600],
    ['上下水认证', '项', 0, 1500, 1500, 1500, 1500, 1500, 1500],
    ['马桶', '个', 0, 800, 800, 800, 800, 800, 800],
    ['排气扇(200*200)', '个', 0, 100, 100, 100, 100, 100, 100],
    ['热水器', '个', 0, 500, 500, 500, 500, 500, 500],
    ['L橱柜+洗碗池', '套', 0, 1500, 1500, 1500, 1500, 1500, 1500],
    ['黑色L橱柜+洗碗池', '套', 0, 1800, 1800, 1800, 1800, 1800, 1800],
    ['吊柜', '项', 0, 500, 500, 500, 500, 500, 500],
    ['墙板特殊颜色', '项', 0, 500, 500, 500, 500, 1000, 1000],
    ['干湿分离', '套', 0, 3000, 3000, 3000, 3000, 3000, 3000],
    ['干湿分离(升级油砂玻璃)', '套', 0, 3500, 3500, 3500, 3500, 3500, 3500],
    ['干湿分离(升级碳晶/竹木)', '套', 0, 3800, 3800, 3800, 3800, 3800, 3800],
    ['扇形卫浴', '套', 0, 2000, 2000, 2000, 2000, 2000, 2000],
    ['螺栓可调节支撑地脚杯', '个', 0, 20, 20, 20, 20, 20, 20],
    ['可调节大支撑腿', '个', 0, 100, 100, 100, 100, 100, 100],
    ['液压杆+绞盘', '套', 0, 500, 500, 500, 500, 500, 500],
    ['玻璃幕墙', '项', 0, 3200, 3200, 3200, 3200, 3200, 3200],
    ['室外露台+屋顶', '项', 0, 4000, 4000, 4000, 4000, 4000, 4000],
    ['楼梯', '项', 0, 2500, 2500, 2500, 2500, 2500, 2500],
    ['拖车', '辆', 16000, 16000, 16000, 16000, 16000, 26000, 26000],
]

RESTRICTED_FOR_X = [
    '屋顶全贴防水卷材', '聚氨酯板75', '聚氨酯底部保温(4cm)', '聚氨酯底部保温(块)', 
    '上下水认证', '马桶', '排气扇(200*200)', '热水器', '螺栓可调节支撑地脚杯', 
    '可调节大支撑腿', '液压杆+绞盘', '玻璃幕墙', '室外露台+屋顶', '通铺屋顶', 
    '楼梯', '墙板特殊颜色', '吊柜', '卫生间配置', '橱柜选择', 
    '踢脚线/顶角线/阴角线', '顶部瓦楞板', '内顶金属雕花板', '平顶', '长城板'
]

# === 翻译字典：将核心词转换为 "Eng / 中文" 格式 ===
TRANS = {
    "基础": "Basic / 基础",
    "装修": "Decor / 装修",
    "门窗": "Door&Win / 门窗",
    "厨卫": "Kitchen&Bath / 厨卫",
    "结构": "Structure / 结构",
    "配件": "Accessories / 配件",
    "认证": "Cert / 认证",
    "升级": "Upgrade / 升级",
    
    # 项目名翻译
    "基础箱体": "Basic Unit / 基础箱体",
    "内部布局": "Layout / 内部布局",
    "保温升级": "Insulation / 保温升级",
    "内墙升级": "Inner Wall / 内墙升级",
    "外墙升级": "Outer Wall / 外墙升级",
    "地板升级": "Floor / 地板升级",
    "入户门": "Main Door / 入户门",
    "室内门": "Inner Door / 室内门",
    "窗户": "Window / 窗户",
    "纱窗": "Screen / 纱窗",
    "卫浴": "Bathroom / 卫浴",
    "橱柜": "Cabinet / 橱柜",
    "马桶": "Toilet / 马桶",
    "热水器": "Water Heater / 热水器",
    "排气扇": "Exhaust Fan / 排气扇",
    "吊柜": "Hanging Cab / 吊柜",
    "墙板特殊颜色": "Special Wall Color / 墙板特殊颜色",
    "屋顶防水": "Roof Waterproof / 屋顶防水",
    "聚氨酯板75": "PU Panel 75 / 聚氨酯板75",
    "底部保温(4cm)": "Bottom PU(4cm) / 底部保温",
    "底部保温(块)": "Bottom PU(Block) / 底部保温块",
    "玻璃幕墙": "Glass Wall / 玻璃幕墙",
    "露台+屋顶": "Terrace / 露台+屋顶",
    "楼梯": "Stairs / 楼梯",
    "通铺屋顶": "Full Roof / 通铺屋顶",
    "液压杆": "Hydraulic Rod / 液压杆",
    "拖车": "Trailer / 拖车",
    "地脚杯": "Foot Cups / 地脚杯",
    "支撑腿": "Support Legs / 支撑腿",
    "踢脚线": "Skirting / 踢脚线",
    "插座认证": "Socket Cert / 插座认证",
    "上下水认证": "Plumbing Cert / 上下水认证",
    "灯具认证": "Light Cert / 灯具认证",
}

def t_cat(k): return TRANS.get(k, k)
def t_item(k): return TRANS.get(k, k)

st.set_page_config(page_title="Global Quotation System", layout="wide")

# 初始化数据
if not os.path.exists(CSV_FILE):
    df_db = pd.DataFrame(default_data, columns=columns)
    df_db.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
else:
    df_db = pd.read_csv(CSV_FILE)

def get_p(item_name, size):
    try:
        if item_name not in df_db['项目名称'].values: return 0.0
        val = df_db.loc[df_db['项目名称'] == item_name, size].values[0]
        return float(val)
    except:
        return 0.0

# ==========================================
# 侧边栏 (Admin)
# ==========================================
st.sidebar.title("🔐 Admin / 管理后台")
admin_pwd = st.sidebar.text_input("Password / 密码", type="password")
IS_ADMIN = (admin_pwd == "123456")

if IS_ADMIN:
    st.sidebar.success("✅ Login Success / 已登录")
    st.sidebar.markdown("### Settings / 设置")
    exchange_rate = st.sidebar.number_input("Exchange Rate (RMB/USD)", 6.0, 8.0, 6.9, 0.05)
    markup_rate = st.sidebar.number_input("Markup / 利润系数", 1.0, 2.5, 1.2, 0.05)
    
    with st.expander("🛠️ Price Editor /底价管理", expanded=False):
        st.warning("Changes are temporary. Download to save permanently. / 修改仅临时生效，请导出保存。")
        edited_df = st.data_editor(df_db, num_rows="dynamic", use_container_width=True, height=600)
        
        if st.button("💾 Save (Temp) / 临时保存"):
            edited_df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
            st.success("Saved! / 已保存")
            st.rerun()
            
        st.markdown("---")
        st.download_button(
            label="📥 Export CSV / 导出价格表",
            data=edited_df.to_csv(index=False, encoding='utf-8-sig'),
            file_name="prices_v3.csv",
            mime="text/csv"
        )
    df_active = edited_df
else:
    exchange_rate = 6.9
    markup_rate = 1.2
    df_active = df_db
    st.sidebar.info("Login to edit prices. / 登录以修改价格。")

# ==========================================
# 主界面
# ==========================================
st.title("🏠 Container House Quotation / 集装箱房屋报价")
bill = []

# --- 1. Basic ---
st.subheader("1. Basic / 基础配置")
c1, c2 = st.columns(2)
with c1:
    size = st.selectbox("Size / 房型尺寸", ['20FT', 'X折叠', 'F700', '10FT', '15FT', '30FT', '40FT'])
    bill.append({"Cat": t_cat("基础"), "Item": t_item("基础箱体"), "Spec": size, "Qty": 1, "RMB": get_p('基础箱体', size)})

with c2:
    if size == "X折叠": opts = ['空箱', '房间数量定制']
    elif size == "40FT": opts = ['空箱', '一室', '两室', '三室', '四室', '五室', '六室', '房间数量定制']
    else: opts = ['空箱', '一室', '两室', '三室', '四室', '房间数量定制']
    layout = st.selectbox("Layout / 内部布局", opts)
    if layout not in ['空箱', '房间数量定制']:
        bill.append({"Cat": t_cat("基础"), "Item": t_item("内部布局"), "Spec": layout, "Qty": 1, "RMB": get_p(layout, size)})

# --- 2. Decoration ---
st.markdown("---")
st.subheader("2. Decoration / 装修")
is_x = (size == "X折叠")

c1, c2, c3 = st.columns(3)
with c1:
    ins = st.selectbox("Insulation / 保温材料", ['岩棉 50mm', '岩棉 75mm', 'eps 75mm', '聚氨酯 75mm'])
    if ins != '岩棉 50mm': bill.append({"Cat": t_cat("装修"), "Item": t_item("保温升级"), "Spec": ins, "Qty": 1, "RMB": get_p(ins, size)})
    
    st.selectbox("Frame Color / 框架颜色", ['White/白色', 'Black/黑色', 'Grey/灰色', 'Custom/定制'])
    wall_col_spec = st.selectbox("Special Wall Color / 墙板特殊颜色", ["No/不需要", "Yes/需要"], disabled=is_x)
    if wall_col_spec == "Yes/需要":
         bill.append({"Cat": t_cat("装修"), "Item": t_item("墙板特殊颜色"), "Spec": "Yes", "Qty": 1, "RMB": get_p('墙板特殊颜色', size)})

with c2:
    in_wall = st.selectbox("Inner Wall / 内墙", ['普通内墙板', '碳晶板(8mm)', '竹木纤维板'])
    if in_wall != '普通内墙板': bill.append({"Cat": t_cat("装修"), "Item": t_item("内墙升级"), "Spec": in_wall, "Qty": 1, "RMB": get_p(in_wall, size)})
    
    out_wall = st.selectbox("Outer Wall / 外墙", ['普通外墙板', '金属雕花板', '长城板'], disabled=(is_x or '长城板' in RESTRICTED_FOR_X and is_x))
    if out_wall != '普通外墙板' and not is_x: bill.append({"Cat": t_cat("装修"), "Item": t_item("外墙升级"), "Spec": out_wall, "Qty": 1, "RMB": get_p(out_wall, size)})

with c3:
    floor = st.selectbox("Floor / 地板", ['地板革(2mm)', '石塑锁扣地板(4cm)'])
    if floor != '地板革(2mm)': bill.append({"Cat": t_cat("装修"), "Item": t_item("地板升级"), "Spec": floor, "Qty": 1, "RMB": get_p(floor, size)})

# --- 3. Doors & Windows ---
st.markdown("---")
st.subheader("3. Doors & Windows / 门窗")
c1, c2, c3 = st.columns(3)
with c1:
    d_main = st.selectbox("Main Door / 入户门", [
        '肯德基双开门', '肯德基单开门', '防盗门1', '防盗门2(钛镁合金)', 
        '断桥铝对开门', '断桥铝单开门', '电动卷帘门', '断桥铝格格单开门', '钢制单开', '定制'])
    bill.append({"Cat": t_cat("门窗"), "Item": t_item("入户门"), "Spec": d_main, "Qty": 1, "RMB": get_p(d_main, size)})

with c2:
    d_inner = st.selectbox("Inner Door / 室内门", ['标配室内门', '高端铝框木芯门', '谷仓门', '木芯门', '定制'])
    if d_inner != '标配室内门': bill.append({"Cat": t_cat("门窗"), "Item": t_item("室内门"), "Spec": d_inner, "Qty": 1, "RMB": get_p(d_inner, size)})

with c3:
    win = st.selectbox("Window / 窗户", ['断桥铝窗(不含纱窗)', '断桥铝推拉窗(含纱窗)', '铝合金推拉窗(含纱窗)', '塑钢平开窗', '塑钢推拉窗', '电动卷帘窗'])
    w_qty = st.number_input("Window Qty / 窗户数量", 0, 10, 2)
    if w_qty > 0: bill.append({"Cat": t_cat("门窗"), "Item": t_item("窗户"), "Spec": win, "Qty": w_qty, "RMB": get_p(win, size)})
    
    scr = st.selectbox("Screen / 纱窗", ['No/不要', 'Common/普通网', 'Steel/金刚网'])
    if '不要' not in scr: bill.append({"Cat": t_cat("门窗"), "Item": t_item("纱窗"), "Spec": scr, "Qty": w_qty if w_qty > 0 else 1, "RMB": get_p(scr.split('/')[-1], size)})

# --- 4. Kitchen & Bath ---
st.markdown("---")
st.subheader("4. Kitchen & Bath / 厨卫")
c1, c2 = st.columns(2)
with c1:
    bath = st.selectbox("Bathroom / 卫生间", ['无', '干湿分离', '干湿分离(升级油砂玻璃)', '干湿分离(升级碳晶/竹木)', '扇形卫浴'], disabled=is_x)
    if bath != '无' and not is_x: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("卫浴"), "Spec": bath, "Qty": 1, "RMB": get_p(bath, size)})
    
    cab = st.selectbox("Cabinet / 橱柜", ['无', 'L橱柜+洗碗池', '黑色L橱柜+洗碗池'], disabled=is_x)
    if cab != '无' and not is_x: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("橱柜"), "Spec": cab, "Qty": 1, "RMB": get_p(cab, size)})

with c2:
    col_a, col_b = st.columns(2)
    with col_a:
        # 1. 标题改成双语 "Upgrade Toilet / 升级马桶"
        opt_toilet = st.selectbox("Upgrade Toilet / 升级马桶", ["No/不需要", "Yes/需要"], disabled=is_x)
        if opt_toilet == "Yes/需要": bill.append({"Cat": t_cat("厨卫"), "Item": t_item("马桶"), "Spec": "Yes", "Qty": 1, "RMB": get_p('马桶', size)})
        
        opt_heater = st.selectbox("Water Heater / 热水器", ["No/不需要", "Yes/需要"], disabled=is_x)
        if opt_heater == "Yes/需要": bill.append({"Cat": t_cat("厨卫"), "Item": t_item("热水器"), "Spec": "Yes", "Qty": 1, "RMB": get_p('热水器', size)})
    with col_b:
        opt_fan = st.selectbox("Exhaust Fan / 排气扇", ["No/不需要", "Yes/需要"], disabled=is_x)
        if opt_fan == "Yes/需要": bill.append({"Cat": t_cat("厨卫"), "Item": t_item("排气扇"), "Spec": "Yes", "Qty": 1, "RMB": get_p('排气扇(200*200)', size)})
        
        opt_h_cab = st.selectbox("Hanging Cab / 吊柜", ["No/不需要", "Yes/需要"], disabled=is_x)
        if opt_h_cab == "Yes/需要": bill.append({"Cat": t_cat("厨卫"), "Item": t_item("吊柜"), "Spec": "Yes", "Qty": 1, "RMB": get_p('吊柜', size)})

# --- 5. Upgrades & Structure ---
st.markdown("---")
st.subheader("5. Upgrades & Structure / 结构与升级")
c1, c2, c3 = st.columns(3)

with c1:
    if st.selectbox("Roof Waterproof / 屋顶防水", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("升级"), "Item": t_item("屋顶防水"), "Spec": "Yes", "Qty": 1, "RMB": get_p('屋顶全贴防水卷材', size)})
    
    if st.selectbox("PU Panel 75 / 聚氨酯板75", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("升级"), "Item": t_item("聚氨酯板75"), "Spec": "Yes", "Qty": 1, "RMB": get_p('聚氨酯板75', size)})
        
    if st.selectbox("Bottom PU(4cm) / 底部保温(4cm)", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("升级"), "Item": t_item("底部保温(4cm)"), "Spec": "Yes", "Qty": 1, "RMB": get_p('聚氨酯底部保温(4cm)', size)})
        
    if st.selectbox("Bottom PU(Block) / 底部保温块", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("升级"), "Item": t_item("底部保温(块)"), "Spec": "Yes", "Qty": 1, "RMB": get_p('聚氨酯底部保温(块)', size)})

with c2:
    if st.selectbox("Glass Wall / 玻璃幕墙", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("结构"), "Item": t_item("玻璃幕墙"), "Spec": "Yes", "Qty": 1, "RMB": get_p('玻璃幕墙', size)})
    
    if st.selectbox("Terrace / 露台+屋顶", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("结构"), "Item": t_item("露台+屋顶"), "Spec": "Yes", "Qty": 1, "RMB": get_p('室外露台+屋顶', size)})
        
    if st.selectbox("Stairs / 楼梯", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("结构"), "Item": t_item("楼梯"), "Spec": "Yes", "Qty": 1, "RMB": get_p('楼梯', size)})
        
    if st.selectbox("Full Roof / 通铺屋顶", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("结构"), "Item": t_item("通铺屋顶"), "Spec": "Yes", "Qty": 1, "RMB": get_p('通铺屋顶', size)})

with c3:
    if st.selectbox("Hydraulic Rod / 液压杆", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("结构"), "Item": t_item("液压杆"), "Spec": "Yes", "Qty": 1, "RMB": get_p('液压杆+绞盘', size)})
        
    if st.selectbox("Trailer / 拖车", ["No/不需要", "Yes/需要"]) == "Yes/需要":
        bill.append({"Cat": t_cat("结构"), "Item": t_item("拖车"), "Spec": "Yes", "Qty": 1, "RMB": get_p('拖车', size)})
    
    qty_foot = st.number_input("Foot Cups / 地脚杯 (Qty)", 0, 20, 0)
    if qty_foot > 0: bill.append({"Cat": t_cat("配件"), "Item": t_item("地脚杯"), "Spec": "Yes", "Qty": qty_foot, "RMB": get_p('螺栓可调节支撑地脚杯', size)})
    
    qty_leg = st.number_input("Support Legs / 支撑腿 (Qty)", 0, 20, 0)
    if qty_leg > 0: bill.append({"Cat": t_cat("配件"), "Item": t_item("支撑腿"), "Spec": "Yes", "Qty": qty_leg, "RMB": get_p('可调节大支撑腿', size)})

# --- 6. Top & Skirting ---
st.markdown("---")
st.subheader("6. Top & Skirting / 顶部与踢脚")
c1, c2 = st.columns(2)
with c1:
    top_opts = st.multiselect("Top Config / 顶部配置", ['顶部瓦楞板', '内顶金属雕花板', '平顶'], disabled=is_x)
    for t in top_opts:
        bill.append({"Cat": t_cat("装修"), "Item": t, "Spec": "Yes", "Qty": 1, "RMB": get_p(t, size)})

with c2:
    skirt = st.selectbox("Skirting / 踢脚线", ['No/无', 'PVC', 'Mn-Al/锰铝合金'], disabled=is_x)
    if '无' not in skirt and not is_x: 
        # 提取 'Mn-Al/锰铝合金' 中的中文部分来查价，或者直接用原始 mapping
        # 简单起见，这里做一个简单的映射查价
        skirt_cn = skirt.split('/')[-1] if '/' in skirt else skirt
        if skirt_cn == '无': skirt_cn = '无' # Fallback
        bill.append({"Cat": t_cat("装修"), "Item": t_item("踢脚线"), "Spec": skirt, "Qty": 1, "RMB": get_p(skirt_cn, size)})

# --- 7. Certification ---
st.markdown("---")
st.subheader("7. Certification / 认证")
c1, c2, c3 = st.columns(3)
with c1:
    opt_wire = st.selectbox("Wire Cert / 电线认证", ["No/不需要", "Yes/需要"])
    if opt_wire == "Yes/需要":
        std = st.selectbox("Wire Std / 标准", ['EU/欧标', 'US/美标', 'AU/澳标'])
        bill.append({"Cat": t_cat("认证"), "Item": t_item("认证电线"), "Spec": std, "Qty": 1, "RMB": get_p('认证电线', size)})
with c2:
    if st.selectbox("Socket Cert / 插座认证", ["No/不需要", "Yes/需要"]) == "Yes/需要":
        bill.append({"Cat": t_cat("认证"), "Item": t_item("插座认证"), "Spec": "Yes", "Qty": 1, "RMB": get_p('认证插座开关', size)})
    if st.selectbox("Plumbing Cert / 上下水认证", ["No/不需要", "Yes/需要"], disabled=is_x) == "Yes/需要":
        bill.append({"Cat": t_cat("认证"), "Item": t_item("上下水认证"), "Spec": "Yes", "Qty": 1, "RMB": get_p('上下水认证', size)})
with c3:
    if st.selectbox("Light Cert / 灯具认证", ["No/不需要", "Yes/需要"]) == "Yes/需要":
        bill.append({"Cat": t_cat("认证"), "Item": t_item("灯具认证"), "Spec": "Yes", "Qty": 1, "RMB": get_p('认证灯', size)})

# ==========================================
# 5. 汇总与输出
# ==========================================
st.markdown("---")
df_res = pd.DataFrame(bill)

if not df_res.empty:
    # 1. 计算总价
    df_res['Total_RMB'] = df_res['Qty'] * df_res['RMB']
    total_rmb = df_res['Total_RMB'].sum()
    total_usd = (total_rmb / exchange_rate) * markup_rate
    
    # 2. 计算有效期 (今天 + 7天)
    valid_date = date.today() + timedelta(days=7)
    
    # 3. 计算 FOB
    fob_price = total_usd + 900

    # --- 显示区域 ---
    st.header(f"💰 Total Price: $ {total_usd:,.2f}")
    
    # [Requirement 3] 增加 EXW 和 有效期说明
    st.caption(f"(EXW Price / 出厂价 | Price Validity: {valid_date} / 价格有效期至: {valid_date})")
    
    # [Requirement 5] 底部增加 FOB
    st.markdown(f"### 🚢 FOB Price / FOB 价格: $ {fob_price:,.2f}")
    
    # [Requirement 4] 英文左，中文右的配置清单
    # 重命名列名以符合双语要求
    df_display = df_res[['Cat', 'Item', 'Spec', 'Qty']].rename(columns={
        "Cat": "Category / 类别", 
        "Item": "Item / 项目", 
        "Spec": "Spec / 规格", 
        "Qty": "Qty / 数量"
    })
    
    if IS_ADMIN:
        with st.expander("🕵️ Cost Detail (Admin Only) / 成本明细"):
            st.dataframe(df_res, use_container_width=True)
            profit = (total_usd * exchange_rate) - total_rmb
            st.success(f"📈 Profit / 预估毛利: ¥ {profit:,.2f}")
    else:
        with st.expander("📄 Configuration List / 配置清单", expanded=True):
            st.table(df_display)
else:
    st.info("Please select items to generate quote. / 请选择配置以生成报价。")
