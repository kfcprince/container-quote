import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

# ==========================================
# 0. 页面初始化配置
# ==========================================
st.set_page_config(
    page_title="Quotation System",
    page_icon="🏠",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 1. 核心数据与多国语言翻译引擎
# ==========================================
CSV_FILE = "prices_v5.csv"
columns = ['项目名称', '单位', 'X折叠', 'F700', '10FT', '15FT', '20FT', '30FT', '40FT']

# 语言选择器
lang_opts = ["Bilingual / 双语", "English", "Español", "Français"]
lang_mode = st.radio("Language / 语言 / Idioma / Langue", lang_opts, horizontal=True, label_visibility="collapsed")

# 小语种专业建材词典
LANG_DICT = {
    "ES": {
        # UI Titles
        "Basic": "Básico", "Decoration": "Decoración", "Doors & Windows": "Puertas y Ventanas",
        "Kitchen & Bath": "Cocina y Baño", "Upgrades & Structure": "Estructura y Mejoras",
        "Top & Skirting": "Techo y Rodapiés", "Certification": "Certificación",
        "Size": "Tamaño", "Layout": "Distribución", "Insulation": "Aislamiento",
        "Frame Color": "Color del marco", "Special Wall Color": "Color de pared especial",
        "Inner Wall": "Pared interior", "Outer Wall": "Pared exterior", "Floor": "Piso",
        "Heating": "Calefacción", "Roof Panel Upgrade": "Mejora del panel de techo",
        "Main Door": "Puerta principal", "Door Color": "Color de puerta", "Inner Door": "Puerta interior",
        "Inner Door Qty": "Cant. de puertas interiores", "Window": "Ventana", "Window Qty": "Cant. de ventanas",
        "Screen": "Mosquitera", "Bathroom": "Baño", "Cabinet": "Armario", "Water Heater": "Calentador de agua",
        "Exhaust Fan": "Extractor de aire", "Hanging Cab": "Armario suspendido",
        "Roof Waterproof": "Impermeabilización de techo", "PU Panel 75": "Panel de PU 75",
        "Bottom PU(4cm)": "PU inferior (4cm)", "Bottom PU(Block)": "PU inferior (Bloque)",
        "Glass Wall": "Pared de vidrio", "Glass Wall Qty": "Cant. pared de vidrio",
        "Outdoor Terrace+Roof": "Terraza exterior + Techo", "Stairs": "Escaleras", "Full Roof": "Techo completo",
        "Hydraulic Rod Qty": "Cant. de varilla hidráulica", "Trailer": "Remolque",
        "Foot Cups": "Copas de pie", "Support Legs": "Patas de apoyo",
        "Top Config": "Config. superior", "Skirting": "Rodapié",
        "Wire Cert": "Cert. de cables", "Wire Std": "Estándar de cable", "Socket Cert": "Cert. de enchufes",
        "Plumbing Cert": "Cert. de plomería", "Light Cert": "Cert. de luces", "Toilet": "Inodoro",
        "Total Price": "Precio Total", "EXW Price": "Precio EXW", "Price Validity": "Validez del precio",
        "FOB Price": "Precio FOB", "Configuration List": "Lista de configuración",
        "Category": "Categoría", "Item": "Artículo", "Spec": "Especificación", "Qty": "Cantidad",
        "Please select items to generate quote.": "Seleccione artículos para generar cotización.",
        
        # Options
        "Empty": "Vacío", "Custom Qty": "Cant. personalizada", "1 Bedroom": "1 Habitación",
        "2 Bedroom": "2 Habitaciones", "3 Bedroom": "3 Habitaciones", "4 Bedroom": "4 Habitaciones",
        "5 Bedroom": "5 Habitaciones", "6 Bedroom": "6 Habitaciones",
        "Yes": "Sí", "No": "No", "None": "Ninguno",
        "White": "Blanco", "Black": "Negro", "Grey": "Gris", "Custom": "Personalizado",
        "Rock Wool 50mm": "Lana de roca 50mm", "Rock Wool 75mm": "Lana de roca 75mm",
        "EPS 75mm": "EPS 75mm", "PU 75mm": "PU 75mm", "PU 100mm": "PU 100mm",
        "Normal": "Normal", "Carbon Crystal(8mm)": "Cristal de carbono (8mm)", "Bamboo Fiber": "Fibra de bambú",
        "Graphene Wall Board": "Panel de pared de grafeno", "Metal Carved": "Metal tallado",
        "WPC Great Wall": "Gran muralla de WPC", "WPC Wall Board": "Panel de pared WPC",
        "Vinyl(2mm)": "Vinilo (2mm)", "SPC(4cm)": "SPC (4cm)", "Graphene Floor Heating": "Suelo radiante de grafeno",
        "Dry-Wet Separate": "Separación seco-húmedo", "Dry-Wet(Frosted Glass)": "Seco-húmedo (Vidrio esmerilado)",
        "Dry-Wet(Carbon/Bamboo)": "Seco-húmedo (Carbono/Bambú)", "Fan-shaped": "Forma de abanico",
        "L-Cabinet+Sink": "Armario en L + Fregadero", "Black L-Cabinet+Sink": "Armario en L negro + Fregadero",
        "Straight Cabinet": "Armario recto", "Common": "Común", "Steel": "Acero", "EU": "Norma UE", "US": "Norma EE.UU.", "AU": "Norma AU"
    },
    "FR": {
        # UI Titles
        "Basic": "Base", "Decoration": "Décoration", "Doors & Windows": "Portes et Fenêtres",
        "Kitchen & Bath": "Cuisine et Bain", "Upgrades & Structure": "Structure et Améliorations",
        "Top & Skirting": "Toit et Plinthes", "Certification": "Certification",
        "Size": "Taille", "Layout": "Agencement", "Insulation": "Isolation",
        "Frame Color": "Couleur du cadre", "Special Wall Color": "Couleur de mur spéciale",
        "Inner Wall": "Mur intérieur", "Outer Wall": "Mur extérieur", "Floor": "Sol",
        "Heating": "Chauffage", "Roof Panel Upgrade": "Amélioration du panneau de toit",
        "Main Door": "Porte principale", "Door Color": "Couleur de porte", "Inner Door": "Porte intérieure",
        "Inner Door Qty": "Qté de portes intérieures", "Window": "Fenêtre", "Window Qty": "Qté de fenêtres",
        "Screen": "Moustiquaire", "Bathroom": "Salle de bain", "Cabinet": "Armoire", "Water Heater": "Chauffe-eau",
        "Exhaust Fan": "Ventilateur d'extraction", "Hanging Cab": "Armoire suspendue",
        "Roof Waterproof": "Imperméabilisation du toit", "PU Panel 75": "Panneau PU 75",
        "Bottom PU(4cm)": "PU inférieur (4cm)", "Bottom PU(Block)": "PU inférieur (Bloc)",
        "Glass Wall": "Mur de verre", "Glass Wall Qty": "Qté mur de verre",
        "Outdoor Terrace+Roof": "Terrasse extérieure + Toit", "Stairs": "Escaliers", "Full Roof": "Toit complet",
        "Hydraulic Rod Qty": "Qté de tige hydraulique", "Trailer": "Remorque",
        "Foot Cups": "Coupes de pied", "Support Legs": "Pieds de support",
        "Top Config": "Config. supérieure", "Skirting": "Plinthe",
        "Wire Cert": "Cert. de fils", "Wire Std": "Norme de fil", "Socket Cert": "Cert. de prises",
        "Plumbing Cert": "Cert. de plomberie", "Light Cert": "Cert. d'éclairage", "Toilet": "Toilettes",
        "Total Price": "Prix Total", "EXW Price": "Prix EXW", "Price Validity": "Validité du prix",
        "FOB Price": "Prix FOB", "Configuration List": "Liste de configuration",
        "Category": "Catégorie", "Item": "Article", "Spec": "Spécification", "Qty": "Quantité",
        "Please select items to generate quote.": "Veuillez sélectionner des articles pour générer un devis.",
        
        # Options
        "Empty": "Vide", "Custom Qty": "Qté personnalisée", "1 Bedroom": "1 Chambre",
        "2 Bedroom": "2 Chambres", "3 Bedroom": "3 Chambres", "4 Bedroom": "4 Chambres",
        "5 Bedroom": "5 Chambres", "6 Bedroom": "6 Chambres",
        "Yes": "Oui", "No": "Non", "None": "Aucun",
        "White": "Blanc", "Black": "Noir", "Grey": "Gris", "Custom": "Personnalisé",
        "Rock Wool 50mm": "Laine de roche 50mm", "Rock Wool 75mm": "Laine de roche 75mm",
        "EPS 75mm": "EPS 75mm", "PU 75mm": "PU 75mm", "PU 100mm": "PU 100mm",
        "Normal": "Normal", "Carbon Crystal(8mm)": "Cristal de carbone (8mm)", "Bamboo Fiber": "Fibre de bambou",
        "Graphene Wall Board": "Panneau mural en graphène", "Metal Carved": "Métal sculpté",
        "WPC Great Wall": "Grande muraille WPC", "WPC Wall Board": "Panneau mural WPC",
        "Vinyl(2mm)": "Vinyle (2mm)", "SPC(4cm)": "SPC (4cm)", "Graphene Floor Heating": "Plancher chauffant graphène",
        "Dry-Wet Separate": "Séparation sec-humide", "Dry-Wet(Frosted Glass)": "Sec-humide (Verre dépoli)",
        "Dry-Wet(Carbon/Bamboo)": "Sec-humide (Carbone/Bambou)", "Fan-shaped": "En forme d'éventail",
        "L-Cabinet+Sink": "Armoire en L + Évier", "Black L-Cabinet+Sink": "Armoire en L noire + Évier",
        "Straight Cabinet": "Armoire droite", "Common": "Commun", "Steel": "Acier", "EU": "Norme UE", "US": "Norme US", "AU": "Norme AU"
    }
}

def t_ui(text):
    """超级多国语言翻译引擎"""
    text_str = str(text)
    if "/" in text_str:
        parts = text_str.split("/")
        eng = parts[0].strip()
        cn = parts[-1].strip()
    else:
        eng = text_str.strip()
        cn = text_str.strip()

    if lang_mode == "Bilingual / 双语":
        return f"{eng} / {cn}" if eng != cn else eng
    elif lang_mode == "English":
        return eng
    elif lang_mode == "Español":
        return LANG_DICT["ES"].get(eng, eng) # 查字典，查不到原样返回英文
    elif lang_mode == "Français":
        return LANG_DICT["FR"].get(eng, eng)
    return eng

# ==========================================
# 底层数据初始化
# ==========================================
default_data = [
    ['无', '项', 0, 0, 0, 0, 0, 0, 0],
    ['不要', '项', 0, 0, 0, 0, 0, 0, 0],
    ['标配室内门', '樘', 0, 0, 0, 0, 0, 0, 0], 
    ['普通内墙板', '套', 0, 0, 0, 0, 0, 0, 0], 
    ['基础箱体', '台', 8000, 19000, 14000, 16000, 21000, 34000, 44000],
    ['空箱', '套', 0, 0, 0, 0, 0, 0, 0],
    ['房间数量定制', '套', 0, 0, 0, 0, 0, 0, 0],
    ['一室', '套', 0, 1000, 1000, 1000, 1000, 1000, 1000],
    ['两室', '套', 0, 2000, 2000, 2000, 2000, 2000, 2000],
    ['三室', '套', 0, 3000, 3000, 3000, 3000, 3000, 3000],
    ['四室', '套', 0, 4000, 4000, 4000, 4000, 4000, 4000],
    ['五室', '套', 0, 5000, 5000, 5000, 5000, 5000, 5000],
    ['六室', '套', 0, 6000, 6000, 6000, 6000, 6000, 6000],
    ['岩棉 50mm', '平米', 0, 0, 0, 0, 0, 0, 0],
    ['岩棉 75mm', '平米', 200, 200, 200, 200, 200, 300, 400],
    ['eps 75mm', '平米', 150, 150, 150, 150, 150, 200, 300],
    ['聚氨酯 75mm', '平米', 0, 6000, 6000, 6000, 6000, 8000, 10000],
    ['100厚聚氨酯', '平米', 0, 0, 0, 0, 0, 0, 21400],
    ['碳晶板(8mm)', '套', 4000, 4000, 2800, 3500, 4000, 4500, 5500],
    ['竹木纤维板', '套', 4000, 4000, 3000, 3500, 3500, 4500, 5500],
    ['聚氨酯板75', '项', 0, 6000, 6000, 6000, 4500, 7000, 9000],
    ['普通外墙板', '套', 0, 0, 0, 0, 0, 0, 0],
    ['金属雕花板', '套', 2500, 2200, 1800, 2100, 2500, 3500, 4500],
    ['长城板', '套', 2500, 2500, 2500, 2500, 2500, 3500, 4500],
    ['石墨烯墙板', '套', 0, 0, 0, 0, 1000, 2000, 3000], 
    ['WPC墙板', '套', 0, 0, 2800, 0, 4000, 6000, 8000], 
    ['木芯门', '樘', 300, 300, 300, 300, 300, 300, 300],
    ['高端铝框木芯门', '樘', 500, 500, 500, 500, 500, 500, 500],
    ['谷仓门', '樘', 1200, 1200, 1200, 1200, 1200, 1200, 1200],
    ['肯德基双开门', '樘', 2200, 2200, 2200, 2200, 2200, 2200, 2200],
    ['肯德基单开门', '樘', 1500, 1500, 1500, 1500, 1500, 1500, 1500],
    ['防盗门1', '樘', 1500, 1500, 1500, 1500, 1500, 1500, 1500],
    ['防盗门2(钛镁合金)', '樘', 4000, 4000, 4000, 4000, 4000, 4000, 4000],
    ['断桥铝对开门', '樘', 2000, 2000, 2000, 2000, 2000, 2000, 2000],
    ['断桥铝单开门', '樘', 1200, 1200, 1200, 1200, 1200, 1200, 1200], 
    ['断桥铝推拉门', '樘', 2000, 2000, 2000, 2000, 2000, 2000, 2000],
    ['钛镁合金推拉门', '樘', 1600, 1600, 1600, 1600, 1600, 1600, 1600],
    ['普通钢制对开门', '樘', 1000, 1000, 1000, 1000, 1000, 1000, 1000], 
    ['电动卷帘门', '樘', 2000, 2000, 2000, 2000, 2000, 2000, 2000],
    ['断桥铝格格单开门', '樘', 1500, 1500, 1500, 1500, 1500, 1500, 1500],
    ['钢制单开', '樘', 500, 500, 500, 500, 500, 500, 500],
    ['断桥铝窗(不含纱窗)', '平米', 450, 450, 450, 450, 450, 450, 450],
    ['断桥铝推拉窗(含纱窗)', '平米', 550, 550, 550, 550, 550, 550, 550],
    ['铝合金推拉窗(含纱窗)', '平米', 300, 300, 300, 300, 300, 300, 300], 
    ['内开内倒窗', '平米', 1200, 1200, 1200, 1200, 1200, 1200, 1200], 
    ['断桥铝对开窗', '平米', 600, 600, 600, 600, 600, 600, 600], 
    ['铝合金外旋(含纱窗)', '平米', 800, 800, 800, 800, 800, 800, 800], 
    ['塑钢平开窗', '平米', 200, 200, 200, 200, 200, 200, 200],
    ['塑钢推拉窗', '平米', 200, 200, 200, 200, 200, 200, 200],
    ['电动卷帘窗', '平米', 650, 650, 650, 650, 650, 650, 650],
    ['普通网', '个', 50, 50, 50, 50, 50, 50, 50],
    ['金刚网', '个', 100, 100, 100, 100, 100, 100, 100],
    ['地板革(2mm)', '套', 300, 700, 600, 800, 800, 1500, 1500],
    ['石塑锁扣地板(4cm)', '套', 1000, 1500, 1200, 1600, 1800, 2500, 3500],
    ['石墨烯地热', '套', 0, 0, 0, 0, 4000, 5000, 6000], 
    ['屋顶全贴防水卷材', '项', 0, 500, 500, 500, 800, 1200, 1800],
    ['聚氨酯底部保温(4cm)', '项', 0, 2500, 2500, 2500, 2500, 4000, 5000],
    ['聚氨酯底部保温(块)', '项', 0, 2000, 2000, 2000, 2000, 3000, 4000],
    ['PVC', '套', 0, 600, 600, 600, 600, 900, 1200],
    ['锰铝合金', '套', 0, 1000, 1000, 1000, 1000, 1300, 1600],
    ['顶部瓦楞板', '套', 0, 1000, 600, 800, 1000, 1500, 2000],
    ['内顶金属雕花板', '套', 0, 500, 500, 500, 500, 800, 1000],
    ['平顶', '套', 0, 1500, 1500, 1500, 1500, 2000, 2500],
    ['通铺屋顶', '项', 0, 4000, 0, 0, 5500, 8500, 11000],
    ['75mm EPS顶板', '项', 0, 0, 0, 0, 1000, 2000, 3000], 
    ['75mm PU顶板', '项', 0, 0, 0, 0, 2000, 3000, 4000], 
    ['100mm EPS顶板', '项', 0, 0, 0, 0, 1000, 1500, 2000],
    ['100mm PU顶板', '项', 0, 0, 0, 0, 2700, 3800, 5400],
    ['100mm顶部框架', '项', 0, 0, 0, 0, 1000, 1500, 2000],
    ['认证电线', '项', 600, 600, 600, 600, 600, 900, 1200], 
    ['认证插座开关', '项', 300, 300, 300, 300, 300, 450, 600], 
    ['认证灯', '项', 200, 200, 200, 200, 200, 300, 400], 
    ['上下水认证', '项', 0, 600, 600, 600, 600, 600, 600], 
    ['马桶', '个', 0, 400, 400, 400, 400, 400, 400], 
    ['排气扇(200*200)', '个', 0, 100, 100, 100, 100, 100, 100],
    ['热水器', '个', 0, 500, 500, 500, 500, 500, 500],
    ['L橱柜+洗碗池', '套', 0, 1800, 1800, 1800, 1800, 1800, 1800], 
    ['黑色L橱柜+洗碗池', '套', 0, 2000, 2000, 2000, 2000, 2000, 2000], 
    ['一字型橱柜', '套', 0, 1200, 1200, 1200, 1200, 1200, 1200], 
    ['吊柜', '项', 0, 600, 600, 600, 600, 600, 600],
    ['干湿分离', '套', 0, 3200, 3200, 3200, 3200, 3200, 3200],
    ['干湿分离(升级油砂玻璃)', '套', 0, 3500, 3500, 3500, 3500, 3500, 3500],
    ['干湿分离(升级碳晶/竹木)', '套', 0, 3700, 3700, 3700, 3700, 3700, 3700],
    ['扇形卫浴', '套', 0, 3200, 3200, 3200, 3200, 3200, 3200],
    ['墙板特殊颜色', '项', 0, 500, 500, 500, 500, 1000, 1000],
    ['螺栓可调节支撑地脚杯', '个', 0, 20, 20, 20, 20, 20, 20],
    ['可调节大支撑腿', '个', 0, 100, 100, 100, 100, 100, 100],
    ['液压杆+绞盘', '套', 0, 500, 500, 500, 500, 500, 500],
    ['玻璃幕墙', '项', 0, 3200, 3200, 3200, 3200, 3200, 3200],
    ['室外露台+屋顶', '项', 0, 4000, 4000, 4000, 5000, 7500, 7500],
    ['楼梯', '项', 0, 2500, 2500, 2500, 2500, 2500, 2500],
    ['拖车', '辆', 0, 0, 0, 0, 16000, 26000, 26000]
]

RESTRICTED_FOR_X = [
    '屋顶全贴防水卷材', '聚氨酯板75', '聚氨酯底部保温(4cm)', '聚氨酯底部保温(块)', 
    '上下水认证', '马桶', '排气扇(200*200)', '热水器', '螺栓可调节支撑地脚杯', 
    '可调节大支撑腿', '液压杆+绞盘', '玻璃幕墙', '室外露台+屋顶', '通铺屋顶', 
    '楼梯', '墙板特殊颜色', '吊柜', '卫生间配置', '橱柜选择', 
    '踢脚线/顶角线/阴角线', '顶部瓦楞板', '内顶金属雕花板', '平顶', '长城板'
]

TRANS = {
    "基础": "Basic / 基础", "装修": "Decor / 装修", "门窗": "Door&Win / 门窗",
    "厨卫": "Kitchen&Bath / 厨卫", "结构": "Structure / 结构", "配件": "Accessories / 配件",
    "认证": "Cert / 认证", "升级": "Upgrade / 升级", "基础箱体": "Basic Unit / 基础箱体",
    "内部布局": "Layout / 内部布局", "保温升级": "Insulation / 保温升级", "内墙升级": "Inner Wall / 内墙升级",
    "外墙升级": "Outer Wall / 外墙升级", "地板升级": "Floor / 地板升级", "入户门": "Main Door / 入户门",
    "室内门": "Inner Door / 室内门", "窗户": "Window / 窗户", "纱窗": "Screen / 纱窗",
    "卫浴": "Bathroom / 卫浴", "橱柜": "Cabinet / 橱柜", "马桶": "Toilet / 马桶",
    "热水器": "Water Heater / 热水器", "排气扇": "Exhaust Fan / 排气扇", "吊柜": "Hanging Cab / 吊柜",
    "墙板特殊颜色": "Special Wall Color / 墙板特殊颜色", "屋顶防水": "Roof Waterproof / 屋顶防水",
    "聚氨酯板75": "PU Panel 75 / 聚氨酯板75", "底部保温(4cm)": "Bottom PU(4cm) / 底部保温",
    "底部保温(块)": "Bottom PU(Block) / 底部保温块", "玻璃幕墙": "Glass Wall / 玻璃幕墙",
    "露台": "Outdoor Terrace+Roof / 室外露台+屋顶", "楼梯": "Stairs / 楼梯", "通铺屋顶": "Full Roof / 通铺屋顶",
    "液压杆": "Hydraulic Rod / 液压杆", "拖车": "Trailer / 拖车", "地脚杯": "Foot Cups / 地脚杯",
    "支撑腿": "Support Legs / 支撑腿", "踢脚线": "Skirting / 踢脚线", "插座认证": "Socket Cert / 插座认证",
    "上下水认证": "Plumbing Cert / 上下水认证", "灯具认证": "Light Cert / 灯具认证", "认证电线": "Wire Cert / 认证电线"
}

def t_cat(k): return t_ui(TRANS.get(k, k))
def t_item(k): return t_ui(TRANS.get(k, k))

def get_cn(text):
    if "/" in str(text): return str(text).split("/")[-1].strip()
    return str(text)

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
st.sidebar.title("🔐 Admin")
admin_pwd = st.sidebar.text_input("Password", type="password", key="admin_pwd_input")
IS_ADMIN = False

if admin_pwd == "HUAhan807810":
    IS_ADMIN = True
    st.sidebar.success("✅ Login Success")
    if st.sidebar.button("Logout"):
        st.session_state.admin_pwd_input = ""
        st.rerun()
    st.sidebar.markdown("### Settings")
    exchange_rate = st.sidebar.number_input("Exchange Rate (RMB/USD)", 6.0, 8.0, 6.7, 0.05, key="ex_rate")
    markup_rate = st.sidebar.number_input("Markup Rate", 1.0, 2.5, 1.2, 0.05, key="mk_rate")
    
    with st.expander("🛠️ Price Editor", expanded=False):
        edited_df = st.data_editor(df_db, num_rows="dynamic", use_container_width=True, height=600, key="editor")
        if st.button("💾 Save (Temp)", key="save_btn"):
            edited_df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
            st.success("Saved!")
            st.rerun()
        st.markdown("---")
        st.download_button(label="📥 Export CSV", data=edited_df.to_csv(index=False, encoding='utf-8-sig'), file_name="prices_v5.csv", mime="text/csv", key="dl_btn")
    df_active = edited_df

elif admin_pwd != "":
    st.sidebar.error("❌ Incorrect Password")
    exchange_rate = 6.7
    markup_rate = 1.2
    df_active = df_db
else:
    exchange_rate = 6.7
    markup_rate = 1.2
    df_active = df_db

# ==========================================
# 主界面 (全部加入 Key，锁死用户选择状态)
# ==========================================
st.title(t_ui("📋 Container House Quotation / 集装箱房屋报价单"))
bill = []

# --- 1. Basic ---
st.subheader(t_ui("1. Basic / 基础配置"))
c1, c2 = st.columns(2)
with c1:
    size_opts = ['20FT', 'X-Folding / X折叠', 'F700', '10FT', '15FT', '30FT', '40FT']
    size_sel = st.selectbox(t_ui("Size / 房型尺寸"), size_opts, format_func=t_ui, key="k_size")
    if "X-Folding" in size_sel: size = "X折叠"
    else: size = size_sel
    bill.append({"Cat": t_cat("基础"), "Item": t_item("基础箱体"), "Spec": t_ui(size_sel), "Qty": 1, "RMB": get_p('基础箱体', size)})

with c2:
    if size == "X折叠": opts = ['Empty / 空箱', 'Custom Qty / 房间数量定制']
    elif size == "40FT": opts = ['Empty / 空箱', '1 Bedroom / 一室', '2 Bedroom / 两室', '3 Bedroom / 三室', '4 Bedroom / 四室', '5 Bedroom / 五室', '6 Bedroom / 六室', 'Custom Qty / 房间数量定制']
    else: opts = ['Empty / 空箱', '1 Bedroom / 一室', '2 Bedroom / 两室', '3 Bedroom / 三室', '4 Bedroom / 四室', 'Custom Qty / 房间数量定制']
    
    layout = st.selectbox(t_ui("Layout / 内部布局"), opts, format_func=t_ui, key="k_layout")
    layout_cn = get_cn(layout)
    if layout_cn not in ['空箱', '房间数量定制']:
        bill.append({"Cat": t_cat("基础"), "Item": t_item("内部布局"), "Spec": t_ui(layout), "Qty": 1, "RMB": get_p(layout_cn, size)})

# --- 2. Decoration ---
st.markdown("---")
st.subheader(t_ui("2. Decoration / 装修"))
is_x = (size == "X折叠")
is_f700 = (size == "F700")

c1, c2, c3 = st.columns(3)
with c1:
    ins_opts = ['Rock Wool 50mm / 岩棉 50mm', 'Rock Wool 75mm / 岩棉 75mm', 'EPS 75mm / eps 75mm', 'PU 75mm / 聚氨酯 75mm']
    if size == '40FT': ins_opts.append('PU 100mm / 100厚聚氨酯')
    ins = st.selectbox(t_ui("Insulation / 保温材料"), ins_opts, format_func=t_ui, key="k_ins")
    ins_cn = get_cn(ins)
    if ins_cn != '岩棉 50mm': bill.append({"Cat": t_cat("装修"), "Item": t_item("保温升级"), "Spec": t_ui(ins), "Qty": 1, "RMB": get_p(ins_cn, size)})
    
    st.selectbox(t_ui("Frame Color / 框架颜色"), ['White / 白色', 'Black / 黑色', 'Grey / 灰色', 'Custom / 定制'], format_func=t_ui, key="k_frame_color")
    wall_col_spec = st.selectbox(t_ui("Special Wall Color / 墙板特殊颜色"), ["No / 不需要", "Yes / 需要"], disabled=is_x, format_func=t_ui, key="k_wall_color")
    if "Yes" in wall_col_spec: bill.append({"Cat": t_cat("装修"), "Item": t_item("墙板特殊颜色"), "Spec": t_ui(wall_col_spec), "Qty": 1, "RMB": get_p('墙板特殊颜色', size)})

with c2:
    in_wall = st.selectbox(t_ui("Inner Wall / 内墙"), ['Normal / 普通内墙板', 'Carbon Crystal(8mm) / 碳晶板(8mm)', 'Bamboo Fiber / 竹木纤维板', 'Graphene Wall Board / 石墨烯墙板'], format_func=t_ui, key="k_in_wall")
    in_wall_cn = get_cn(in_wall)
    if in_wall_cn != '普通内墙板': bill.append({"Cat": t_cat("装修"), "Item": t_item("内墙升级"), "Spec": t_ui(in_wall), "Qty": 1, "RMB": get_p(in_wall_cn, size)})
    
    out_wall = st.selectbox(t_ui("Outer Wall / 外墙"), ['Normal / 普通外墙板', 'Metal Carved / 金属雕花板', 'WPC Great Wall / 长城板', 'WPC Wall Board / WPC墙板'], disabled=(is_x or '长城板' in RESTRICTED_FOR_X and is_x), format_func=t_ui, key="k_out_wall")
    out_wall_cn = get_cn(out_wall)
    if out_wall_cn != '普通外墙板' and not is_x: bill.append({"Cat": t_cat("装修"), "Item": t_item("外墙升级"), "Spec": t_ui(out_wall), "Qty": 1, "RMB": get_p(out_wall_cn, size)})

with c3:
    floor = st.selectbox(t_ui("Floor / 地板"), ['Vinyl(2mm) / 地板革(2mm)', 'SPC(4cm) / 石塑锁扣地板(4cm)'], format_func=t_ui, key="k_floor")
    floor_cn = get_cn(floor)
    bill.append({"Cat": t_cat("装修"), "Item": t_item("地板升级"), "Spec": t_ui(floor), "Qty": 1, "RMB": get_p(floor_cn, size)})
    
    heating = st.selectbox(t_ui("Heating / 供暖"), ['No / 无', 'Graphene Floor Heating / 石墨烯地热'], disabled=is_x, format_func=t_ui, key="k_heating")
    heating_cn = get_cn(heating)
    if heating_cn != '无' and not is_x: bill.append({"Cat": t_cat("装修"), "Item": t_ui("Graphene Floor Heating / 石墨烯地热"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('石墨烯地热', size)})

    roof_panel_opts = ['None / 无', '75mm EPS / 75mm EPS顶板', '75mm PU / 75mm PU顶板', '100mm EPS / 100mm EPS顶板', '100mm PU / 100mm PU顶板', '100mm Frame / 100mm顶部框架']
    roof_panel = st.selectbox(t_ui("Roof Panel Upgrade / 顶板升级"), roof_panel_opts, disabled=is_x, format_func=t_ui, key="k_roof_panel")
    roof_panel_cn = get_cn(roof_panel)
    if roof_panel_cn != '无' and not is_x: bill.append({"Cat": t_cat("升级"), "Item": t_ui("Roof Panel Upgrade / 顶板升级"), "Spec": t_ui(roof_panel), "Qty": 1, "RMB": get_p(roof_panel_cn, size)})

# --- 3. Doors & Windows ---
st.markdown("---")
st.subheader(t_ui("3. Doors & Windows / 门窗"))
c1, c2, c3 = st.columns(3)
with c1:
    d_main_opts = ['Commercial Alum. Door (Double) / 肯德基双开门', 'Commercial Alum. Door (Single) / 肯德基单开门', 'Steel Security Door (Type A) / 防盗门1', 'Ti-Mg Alloy Security Door / 防盗门2(钛镁合金)', 'Thermal Break Alum. Door (Double) / 断桥铝对开门', 'Thermal Break Alum. Door (Single) / 断桥铝单开门', 'Thermal Break Sliding Door / 断桥铝推拉门', 'Ti-Mg Alloy Sliding Door / 钛镁合金推拉门', 'Normal Steel Double Door / 普通钢制对开门', 'Electric Roller Shutter / 电动卷帘门', 'Thermal Break Door w/ Grids / 断桥铝格格单开门', 'Single Steel Door / 钢制单开', 'Custom / 定制']
    d_main = st.selectbox(t_ui("Main Door / 入户门"), d_main_opts, format_func=t_ui, key="k_d_main")
    d_color = st.selectbox(t_ui("Door Color / 颜色"), ['Black / 黑色', 'White / 白色', 'Grey / 灰色'], format_func=t_ui, key="k_d_color")
    full_spec = f"{t_ui(d_main)} (Color: {t_ui(d_color)})"
    bill.append({"Cat": t_cat("门窗"), "Item": t_item("入户门"), "Spec": full_spec, "Qty": 1, "RMB": get_p(get_cn(d_main), size)})

with c2:
    d_inner_opts = ['Standard / 标配室内门', 'High-end Alum. Frame / 高端铝框木芯门', 'Barn Door / 谷仓门', 'Wood Core / 木芯门', 'Custom / 定制']
    d_inner = st.selectbox(t_ui("Inner Door / 室内门"), d_inner_opts, format_func=t_ui, key="k_d_inner")
    d_inner_qty = st.number_input(t_ui("Inner Door Qty / 室内门数量"), 0, 10, 1 if "Standard" not in d_inner else 0, key="k_d_inner_qty")
    d_inner_cn = get_cn(d_inner)
    if d_inner_cn != '标配室内门' and d_inner_qty > 0: bill.append({"Cat": t_cat("门窗"), "Item": t_item("室内门"), "Spec": t_ui(d_inner), "Qty": d_inner_qty, "RMB": get_p(d_inner_cn, size)})

with c3:
    win_opts = ['Thermal Break(No Screen) / 断桥铝窗(不含纱窗)', 'Thermal Break Sliding(w/ Screen) / 断桥铝推拉窗(含纱窗)', 'Tilt & Turn Window / 内开内倒窗', 'Thermal Break Double Window / 断桥铝对开窗', 'Alum. Outward Swing(w/ Screen) / 铝合金外旋(含纱窗)', 'Alum. Sliding(w/ Screen) / 铝合金推拉窗(含纱窗)', 'PVC Swing / 塑钢平开窗', 'PVC Sliding / 塑钢推拉窗', 'Electric Rolling / 电动卷帘窗']
    win = st.selectbox(t_ui("Window / 窗户"), win_opts, format_func=t_ui, key="k_win")
    w_qty = st.number_input(t_ui("Window Qty / 窗户数量"), 0, 10, 2, key="k_w_qty")
    if w_qty > 0: bill.append({"Cat": t_cat("门窗"), "Item": t_item("窗户"), "Spec": t_ui(win), "Qty": w_qty, "RMB": get_p(get_cn(win), size)})
    scr = st.selectbox(t_ui("Screen / 纱窗"), ['No / 不要', 'Common / 普通网', 'Steel / 金刚网'], format_func=t_ui, key="k_scr")
    scr_cn = get_cn(scr)
    if '不要' not in scr_cn: bill.append({"Cat": t_cat("门窗"), "Item": t_item("纱窗"), "Spec": t_ui(scr), "Qty": w_qty if w_qty > 0 else 1, "RMB": get_p(scr_cn, size)})

# --- 4. Kitchen & Bath ---
st.markdown("---")
st.subheader(t_ui("4. Kitchen & Bath / 厨卫"))
disable_kb = (is_x or is_f700)
c1, c2 = st.columns(2)
with c1:
    bath_opts = ['None / 无', 'Dry-Wet Separate / 干湿分离', 'Dry-Wet(Frosted Glass) / 干湿分离(升级油砂玻璃)', 'Dry-Wet(Carbon/Bamboo) / 干湿分离(升级碳晶/竹木)', 'Fan-shaped / 扇形卫浴']
    bath = st.selectbox(t_ui("Bathroom / 卫生间"), bath_opts, disabled=disable_kb, format_func=t_ui, key="k_bath")
    bath_cn = get_cn(bath)
    if bath_cn != '无' and not disable_kb: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("卫浴"), "Spec": t_ui(bath), "Qty": 1, "RMB": get_p(bath_cn, size)})
    
    cab_opts = ['None / 无', 'L-Cabinet+Sink / L橱柜+洗碗池', 'Black L-Cabinet+Sink / 黑色L橱柜+洗碗池', 'Straight Cabinet / 一字型橱柜']
    cab = st.selectbox(t_ui("Cabinet / 橱柜"), cab_opts, disabled=disable_kb, format_func=t_ui, key="k_cab")
    cab_cn = get_cn(cab)
    if cab_cn != '无' and not disable_kb: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("橱柜"), "Spec": t_ui(cab), "Qty": 1, "RMB": get_p(cab_cn, size)})

with c2:
    col_a, col_b = st.columns(2)
    with col_a:
        opt_heater = st.selectbox(t_ui("Water Heater / 热水器"), ["No / 不需要", "Yes / 需要"], disabled=disable_kb, format_func=t_ui, key="k_heater")
        if "Yes" in opt_heater and not disable_kb: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("热水器"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('热水器', size)})
    with col_b:
        opt_fan = st.selectbox(t_ui("Exhaust Fan / 排气扇"), ["No / 不需要", "Yes / 需要"], disabled=disable_kb, format_func=t_ui, key="k_fan")
        if "Yes" in opt_fan and not disable_kb: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("排气扇"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('排气扇(200*200)', size)})
        opt_h_cab = st.selectbox(t_ui("Hanging Cab / 吊柜"), ["No / 不需要", "Yes / 需要"], disabled=disable_kb, format_func=t_ui, key="k_hcab")
        if "Yes" in opt_h_cab and not disable_kb: bill.append({"Cat": t_cat("厨卫"), "Item": t_item("吊柜"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('吊柜', size)})

# --- 5. Upgrades & Structure ---
st.markdown("---")
st.subheader(t_ui("5. Upgrades & Structure / 结构与升级"))
disable_struct = is_x 
allow_opts = ['20FT', '30FT', '40FT']
disable_special = (size not in allow_opts)

c1, c2, c3 = st.columns(3)
with c1:
    if "Yes" in st.selectbox(t_ui("Roof Waterproof / 屋顶防水"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_waterproof"): bill.append({"Cat": t_cat("升级"), "Item": t_item("屋顶防水"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('屋顶全贴防水卷材', size)})
    if "Yes" in st.selectbox(t_ui("PU Panel 75 / 聚氨酯板75"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_pu75"): bill.append({"Cat": t_cat("升级"), "Item": t_item("聚氨酯板75"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('聚氨酯板75', size)})
    if "Yes" in st.selectbox(t_ui("Bottom PU(4cm) / 底部保温(4cm)"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_b_pu4"): bill.append({"Cat": t_cat("升级"), "Item": t_item("底部保温(4cm)"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('聚氨酯底部保温(4cm)', size)})
    if "Yes" in st.selectbox(t_ui("Bottom PU(Block) / 底部保温(块)"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_b_publock"): bill.append({"Cat": t_cat("升级"), "Item": t_item("底部保温(块)"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('聚氨酯底部保温(块)', size)})

with c2:
    g_wall_opt = st.selectbox(t_ui("Glass Wall / 玻璃幕墙"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_glass_w")
    if "Yes" in g_wall_opt and not disable_struct:
        g_wall_qty = st.number_input(t_ui("Glass Wall Qty / 玻璃幕墙数量"), 1, 10, 1, key="k_glass_qty")
        bill.append({"Cat": t_cat("结构"), "Item": t_item("玻璃幕墙"), "Spec": t_ui("Yes / 需要"), "Qty": g_wall_qty, "RMB": get_p('玻璃幕墙', size)})
    if "Yes" in st.selectbox(t_ui("Outdoor Terrace+Roof / 室外露台+屋顶"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_terrace"): bill.append({"Cat": t_cat("结构"), "Item": t_item("露台"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('室外露台+屋顶', size)})
    if "Yes" in st.selectbox(t_ui("Stairs / 楼梯"), ["No / 不需要", "Yes / 需要"], disabled=disable_struct, format_func=t_ui, key="k_stairs"): bill.append({"Cat": t_cat("结构"), "Item": t_item("楼梯"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('楼梯', size)})
    is_frozen_roof = disable_struct or disable_special
    if "Yes" in st.selectbox(t_ui("Full Roof / 通铺屋顶"), ["No / 不需要", "Yes / 需要"], disabled=is_frozen_roof, format_func=t_ui, key="k_fullroof"): bill.append({"Cat": t_cat("结构"), "Item": t_item("通铺屋顶"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('通铺屋顶', size)})

with c3:
    h_rod_qty = st.number_input(t_ui("Hydraulic Rod Qty / 液压杆数量 (0-4)"), 0, 4, 0, disabled=disable_struct, key="k_rod")
    if h_rod_qty > 0 and not disable_struct: bill.append({"Cat": t_cat("结构"), "Item": t_item("液压杆"), "Spec": f"{h_rod_qty}", "Qty": h_rod_qty, "RMB": get_p('液压杆+绞盘', size)})
    is_frozen_trailer = disable_special 
    if "Yes" in st.selectbox(t_ui("Trailer / 拖车"), ["No / 不需要", "Yes / 需要"], disabled=is_frozen_trailer, format_func=t_ui, key="k_trailer"): bill.append({"Cat": t_cat("结构"), "Item": t_item("拖车"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('拖车', size)})
    qty_foot = st.number_input(t_ui("Foot Cups / 地脚杯 (Qty)"), 0, 20, 0, disabled=is_x, key="k_foot")
    if qty_foot > 0: bill.append({"Cat": t_cat("配件"), "Item": t_item("地脚杯"), "Spec": t_ui("Yes / 需要"), "Qty": qty_foot, "RMB": get_p('螺栓可调节支撑地脚杯', size)})
    qty_leg = st.number_input(t_ui("Support Legs / 支撑腿 (Qty)"), 0, 20, 0, disabled=is_x, key="k_leg")
    if qty_leg > 0: bill.append({"Cat": t_cat("配件"), "Item": t_item("支撑腿"), "Spec": t_ui("Yes / 需要"), "Qty": qty_leg, "RMB": get_p('可调节大支撑腿', size)})

# --- 6. Top & Skirting ---
st.markdown("---")
st.subheader(t_ui("6. Top & Skirting / 顶部与踢脚"))
disable_top_all = is_x
c1, c2 = st.columns(2)
with c1:
    raw_top_opts = ['Corrugated Board / 顶部瓦楞板', 'Metal Carved Board / 内顶金属雕花板', 'Flat Top / 平顶']
    if is_f700: raw_top_opts = [opt for opt in raw_top_opts if 'Flat Top' not in opt]
    top_opts = st.multiselect(t_ui("Top Config / 顶部配置"), raw_top_opts, disabled=disable_top_all, format_func=t_ui, key="k_top_cfg")
    for t in top_opts:
        t_cn = get_cn(t)
        bill.append({"Cat": t_cat("装修"), "Item": t_ui(t), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p(t_cn, size)})

with c2:
    skirt = st.selectbox(t_ui("Skirting / 踢脚线"), ['No / 无', 'PVC', 'Mn-Al / 锰铝合金'], disabled=disable_top_all, format_func=t_ui, key="k_skirt")
    skirt_cn = get_cn(skirt)
    if skirt_cn != '无' and not disable_top_all: bill.append({"Cat": t_cat("装修"), "Item": t_item("踢脚线"), "Spec": t_ui(skirt), "Qty": 1, "RMB": get_p(skirt_cn, size)})

# --- 7. Certification ---
st.markdown("---")
st.subheader(t_ui("7. Certification / 认证"))
c1, c2, c3 = st.columns(3)
with c1:
    opt_wire = st.selectbox(t_ui("Wire Cert / 电线认证"), ["No / 不需要", "Yes / 需要"], format_func=t_ui, key="k_wire_cert")
    if "Yes" in opt_wire:
        std = st.selectbox(t_ui("Wire Std / 标准"), ['EU / 欧标', 'US / 美标', 'AU / 澳标'], format_func=t_ui, key="k_wire_std")
        bill.append({"Cat": t_cat("认证"), "Item": t_item("认证电线"), "Spec": t_ui(std), "Qty": 1, "RMB": get_p('认证电线', size)})
with c2:
    if "Yes" in st.selectbox(t_ui("Socket Cert / 插座认证"), ["No / 不需要", "Yes / 需要"], format_func=t_ui, key="k_sock_cert"): bill.append({"Cat": t_cat("认证"), "Item": t_item("插座认证"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('认证插座开关', size)})
    if "Yes" in st.selectbox(t_ui("Plumbing Cert / 上下水认证"), ["No / 不需要", "Yes / 需要"], disabled=is_x, format_func=t_ui, key="k_plumb_cert"): bill.append({"Cat": t_cat("认证"), "Item": t_item("上下水认证"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('上下水认证', size)})
with c3:
    if "Yes" in st.selectbox(t_ui("Light Cert / 灯具认证"), ["No / 不需要", "Yes / 需要"], format_func=t_ui, key="k_light_cert"): bill.append({"Cat": t_cat("认证"), "Item": t_item("灯具认证"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('认证灯', size)})
    opt_toilet_cert = st.selectbox(t_ui("Toilet / 马桶"), ["No / 不需要", "Yes / 需要"], disabled=is_x, format_func=t_ui, key="k_toilet")
    if "Yes" in opt_toilet_cert and not is_x: bill.append({"Cat": t_cat("认证"), "Item": t_ui("Toilet / 马桶"), "Spec": t_ui("Yes / 需要"), "Qty": 1, "RMB": get_p('马桶', size)})

# ==========================================
# 5. 汇总
# ==========================================
st.markdown("---")
df_res = pd.DataFrame(bill)

if not df_res.empty:
    df_res['Total_RMB'] = df_res['Qty'] * df_res['RMB']
    total_rmb = df_res['Total_RMB'].sum()
    total_usd = (total_rmb / exchange_rate) * markup_rate
    valid_date = date.today() + timedelta(days=7)
    fob_price = total_usd + 900

    st.header(f"💰 {t_ui('Total Price / 预估总价')}: $ {total_usd:,.2f}")
    st.markdown(f"#### ({t_ui('EXW Price / 出厂价')} | {t_ui('Price Validity / 价格有效期至')}: {valid_date})")
    
    df_display = df_res[['Cat', 'Item', 'Spec', 'Qty']].rename(columns={
        "Cat": t_ui("Category / 类别"), "Item": t_ui("Item / 项目"), "Spec": t_ui("Spec / 规格"), "Qty": t_ui("Qty / 数量")
    })
    
    if IS_ADMIN:
        with st.expander("🕵️ Cost Detail (Admin Only)"):
            st.dataframe(df_res, use_container_width=True)
            profit = (total_usd * exchange_rate) - total_rmb
            st.success(f"📈 Profit / 预估毛利: ¥ {profit:,.2f}")
    else:
        with st.expander(t_ui("Configuration List / 配置清单"), expanded=True):
            st.table(df_display)

    st.caption(f"🚢 {t_ui('FOB Price / FOB 价格')} : $ {fob_price:,.2f}")
else:
    st.info(t_ui("Please select items to generate quote. / 请选择配置以生成报价。"))
