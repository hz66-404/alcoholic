


# import streamlit as st
# import json
# import os
# from PIL import Image, ExifTags

# # ✅ 文本字典
# t_dict = {
#     "zh": {
#         "page_title": "🍇 酒识广场",
#         "main_title": "🍇 酒识广场",
#         "caption": "浏览大家分享的美酒！",
#         "no_data": "目前还没有酒的分享，快点击右下角 ➕ 上传吧！",
#         "origin": "产地",
#         "price": "价格",
#         "store": "购买渠道",
#         "description": "描述",
#         "rating": "推荐指数",
#         "created_at": "上传时间",
#         "language": "🌐 语言 / Language",
#         "back_home": "返回首页"
#     },
#     "en": {
#         "page_title": "🍇 Wine Sharing Plaza",
#         "main_title": "🍇 Wine Sharing Plaza",
#         "caption": "Browse wines shared by everyone!",
#         "no_data": "No wine shared yet. Click ➕ at the bottom right to upload!",
#         "origin": "Origin",
#         "price": "Price",
#         "store": "Store",
#         "description": "Description",
#         "rating": "Rating",
#         "created_at": "Created at",
#         "language": "🌐 Language / 语言",
#         "back_home": "Back to Home"
#     }
# }

# # ✅ 页面设置
# st.set_page_config(layout="wide")

# # ✅ 获取语言参数并切换
# query_lang = st.query_params.get("lang", ["zh"])[0]
# lang = "en" if query_lang == "en" else "zh"
# t = t_dict[lang]

# # ✅ 显示语言选择栏
# lang_display = st.sidebar.selectbox(
#     label=t_dict["zh"]["language"],
#     options=["中文", "English"],
#     index=0 if lang == "zh" else 1,
#     key="language_switch"
# )
# lang = "zh" if lang_display == "中文" else "en"

# st.query_params["lang"] = lang

# t = t_dict[lang]

# st.title(t["main_title"])
# st.caption(t["caption"])

# # ✅ 加载数据
# DATA_FILE = "wine_data.json"
# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r") as f:
#         wine_data = json.load(f)
# else:
#     wine_data = []

# # ✅ 图像方向处理
# def load_image_with_correct_orientation(path):
#     image = Image.open(path)
#     try:
#         for orientation in ExifTags.TAGS.keys():
#             if ExifTags.TAGS[orientation] == 'Orientation':
#                 break
#         exif = image._getexif()
#         if exif is not None:
#             orientation_value = exif.get(orientation, None)
#             if orientation_value == 3:
#                 image = image.rotate(180, expand=True)
#             elif orientation_value == 6:
#                 image = image.rotate(270, expand=True)
#             elif orientation_value == 8:
#                 image = image.rotate(90, expand=True)
#     except:
#         pass
#     return image

# # ✅ 显示酒卡片
# if not wine_data:
#     st.info(t["no_data"])
# else:
#     cols = st.columns(2)
#     for idx, item in enumerate(wine_data):
#         with cols[idx % 2]:
#             img = load_image_with_correct_orientation(item["image"])
#             st.image(img, use_container_width=True)

#             st.markdown(f"**{item['wine_name']}** ({item['year']})")
#             currency = item.get("currency", "¥")  # 默认人民币符号
#             st.markdown(f"📍 {item['origin'] or 'N/A'} ｜ 💰 {currency}{item['price']:.2f}")
#             st.markdown(f"🛒 {item['store'] or 'N/A'}")
#             if item.get("description"):
#                 st.markdown(f"💬 {item['description']}")

#             rating = item.get("rating", 0)
#             stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
#             st.markdown(f"🌟 {t['rating']}：{stars}")
#             st.caption(f"🕒 {t['created_at']}：{item['created_at']}")

# # ✅ 固定右下角上传按钮（跳转时带上 lang 参数）
# st.markdown(
#     f"""
#     <style>
#     .plus-button {{
#         position: fixed;
#         bottom: 30px;
#         right: 30px;
#         background-color: #ff4b4b;
#         color: white;
#         border: none;
#         border-radius: 50%;
#         width: 60px;
#         height: 60px;
#         font-size: 36px;
#         text-align: center;
#         line-height: 60px;
#         cursor: pointer;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.3);
#         z-index: 9999;
#     }}
#     </style>
#     <a href="/upload?lang={lang}" target="_self">
#         <div class="plus-button">＋</div>
#     </a>
#     """,
#     unsafe_allow_html=True
# )




import streamlit as st
from PIL import Image, ExifTags
from supabase import create_client, Client
import requests
import io
import base64

# ✅ Supabase 配置
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ 文本字典
t_dict = {
    "zh": {
        "page_title": "🍇 酒识广场",
        "main_title": "🍇 酒识广场",
        "caption": "浏览大家分享的美酒！",
        "no_data": "目前还没有酒的分享，快点击右下角 ➕ 上传吧！",
        "origin": "产地",
        "price": "价格",
        "store": "购买渠道",
        "description": "描述",
        "rating": "推荐指数",
        "created_at": "上传时间",
        "language": "🌐 语言 / Language",
        "back_home": "返回首页"
    },
    "en": {
        "page_title": "🍇 Wine Sharing Plaza",
        "main_title": "🍇 Wine Sharing Plaza",
        "caption": "Browse wines shared by everyone!",
        "no_data": "No wine shared yet. Click ➕ at the bottom right to upload!",
        "origin": "Origin",
        "price": "Price",
        "store": "Store",
        "description": "Description",
        "rating": "Rating",
        "created_at": "Created at",
        "language": "🌐 Language / 语言",
        "back_home": "Back to Home"
    }
}

# ✅ 页面设置
st.set_page_config(layout="wide")

# ✅ 获取语言参数并切换
query_lang = st.query_params.get("lang", ["zh"])[0]
lang = "en" if query_lang == "en" else "zh"
t = t_dict[lang]

# ✅ 显示语言选择栏
lang_display = st.sidebar.selectbox(
    label=t_dict["zh"]["language"],
    options=["中文", "English"],
    index=0 if lang == "zh" else 1,
    key="language_switch"
)
lang = "zh" if lang_display == "中文" else "en"
st.query_params["lang"] = lang
t = t_dict[lang]

st.title(t["main_title"])
st.caption(t["caption"])

# ✅ 图像方向处理
def load_image_with_correct_orientation(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except:
        pass
    return image

# ✅ 加载数据
response = supabase.table("wine_data").select("*").order("created_at", desc=True).execute()
wine_data = response.data if response.data else []

# ✅ 显示酒卡片
if not wine_data:
    st.info(t["no_data"])
else:
    cols = st.columns(3)
    for idx, item in enumerate(wine_data):
        with cols[idx % 3]:
            # 加载 Supabase 图片
            image_path = item["image"]
            st.image(image_path, use_container_width=True)

            st.markdown(f"**{item['wine_name']}** ({item['year']})")
            currency = item.get("currency", "¥")
            st.markdown(f"📍 {item['origin'] or 'N/A'} ｜ 💰 {currency}{item['price']:.2f}")
            st.markdown(f"🛒 {item['store'] or 'N/A'}")
            if item.get("description"):
                st.markdown(f"💬 {item['description']}")

            rating = item.get("rating", 0)
            stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
            st.markdown(f"🌟 {t['rating']}：{stars}")
            st.caption(f"🕒 {t['created_at']}：{item['created_at']}")

# ✅ 固定右下角上传按钮
st.markdown(
    f"""
    <style>
    .plus-button {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 36px;
        text-align: center;
        line-height: 60px;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        z-index: 9999;
    }}
    </style>
    <a href="/upload?lang={lang}" target="_self">
        <div class="plus-button">＋</div>
    </a>
    """,
    unsafe_allow_html=True
)
