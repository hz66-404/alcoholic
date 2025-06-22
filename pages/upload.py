

# import streamlit as st
# import os
# import json
# from datetime import datetime
# import streamlit.components.v1 as components
# from streamlit_js_eval import streamlit_js_eval  # 用于获取星星评分

# # ✅ 文本字典（支持中英文）
# t_dict = {
#     "zh": {
#         "title": "📤 上传一瓶你喜欢的酒",
#         "wine_name": "酒名",
#         "year": "年份",
#         "origin": "产地",
#         "price": "价格",
#         "store": "购买地点",
#         "description": "你为什么喜欢这瓶酒？（选填）",
#         "photo": "上传酒瓶照片",
#         "submit": "提交",
#         "warning": "请填写酒名并上传照片！",
#         "success": "✅ 上传成功！返回主页查看吧～",
#         "back_home": "⬅ 返回首页",
#         "rating": "推荐指数",
#         "currency": "货币",
#         "currency_options": ["人民币 (¥)", "美元 ($)", "欧元 (€)"]
#     },
#     "en": {
#         "title": "📤 Upload Your Favorite Wine",
#         "wine_name": "Wine Name",
#         "year": "Year",
#         "origin": "Origin",
#         "price": "Price",
#         "store": "Store",
#         "description": "Why do you like this wine? (optional)",
#         "photo": "Upload Wine Photo",
#         "submit": "Submit",
#         "warning": "Please fill in wine name and upload photo!",
#         "success": "✅ Upload successful! Check it on the home page!",
#         "back_home": "⬅ Back to Home",
#         "rating": "Rating",
#         "currency": "Currency",
#         "currency_options": ["CNY (¥)", "USD ($)", "EUR (€)"]
#     }
# }

# # ✅ 根据 URL 参数判断使用中文还是英文
# query_params = st.query_params if hasattr(st, 'query_params') else st.experimental_get_query_params()
# lang = query_params.get("lang", ["zh"])[0]

# # ✅ 根据 lang 选择对应的文本字典（默认为中文）
# if lang == "e":
#     t = t_dict["en"]
# else:
#     t = t_dict["zh"]

# # ✅ 页面设置
# st.set_page_config(page_title=t["title"], layout="centered")
# st.title(t["title"])

# # ✅ 显示评分组件
# st.markdown(f"### 🌟 {t['rating']}")
# components.html("""
# <style>
#   .star-rating {
#     font-size: 36px;
#     unicode-bidi: bidi-override;
#     direction: ltr;
#   }
#   .star {
#     display: inline-block;
#     color: #ccc;
#     cursor: pointer;
#   }
# </style>
# <div class="star-rating">
#   <span class="star" onclick="setRating(1)">★</span>
#   <span class="star" onclick="setRating(2)">★</span>
#   <span class="star" onclick="setRating(3)">★</span>
#   <span class="star" onclick="setRating(4)">★</span>
#   <span class="star" onclick="setRating(5)">★</span>
# </div>
# <script>
#   function setRating(val) {
#     localStorage.setItem("rating", val);
#     const stars = document.querySelectorAll(".star");
#     stars.forEach((star, index) => {
#       star.style.color = index < val ? "gold" : "#ccc";
#     });
#   }
# </script>
# """, height=50)

# # ✅ 获取评分值
# rating = streamlit_js_eval(js_expressions="localStorage.getItem('rating')", key="get_rating")
# rating_value = int(rating) if rating and rating.isdigit() else 0

# # ✅ 数据路径
# UPLOAD_FOLDER = "uploaded_images"
# DATA_FILE = "wine_data.json"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r") as f:
#         wine_data = json.load(f)
# else:
#     wine_data = []


# # ✅ 上传表单
# with st.form("upload_form", clear_on_submit=True):
#     wine_name = st.text_input(t["wine_name"])
#     year = st.number_input(t["year"], min_value=1900, max_value=datetime.now().year, value=2020)
#     origin = st.text_input(t["origin"])
#     # price = st.number_input(f"{t['price']} {currency_symbol}", min_value=0.0, step=0.1, key="price_input")
#      # ✅ 两列：价格 + 货币
#     col1, col2 = st.columns([2, 1])
#     with col1:
#         price = st.number_input(t["price"], min_value=0.0, step=0.1, key="price_input")
#     with col2:
#         currency_selection = st.selectbox(t["currency"], t["currency_options"], index=0, key="currency_select")
#     currency_symbol = currency_selection.split("(")[-1].replace(")", "")
#     store = st.text_input(t["store"])
#     description = st.text_area(t["description"], height=100)
#     photo = st.file_uploader(t["photo"], type=["jpg", "jpeg", "png"])
#     submitted = st.form_submit_button(t["submit"])

#     if submitted:
#         if not wine_name or not photo:
#             st.warning(t["warning"])
#         else:
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             filename = f"{timestamp}_{photo.name}"
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             with open(filepath, "wb") as f:
#                 f.write(photo.read())

#             entry = {
#                 "wine_name": wine_name,
#                 "year": int(year),
#                 "origin": origin,
#                 "price": float(price),
#                 "currency": currency_symbol,
#                 "store": store,
#                 "description": description,
#                 "image": filepath,
#                 "created_at": timestamp,
#                 "rating": rating_value
#             }

#             wine_data.insert(0, entry)
#             with open(DATA_FILE, "w") as f:
#                 json.dump(wine_data, f, indent=2, ensure_ascii=False)

#             st.success(t["success"])
#             home_url = f"/?lang={lang}"
#             st.markdown(f"[🏠 {t['back_home']}]({home_url})", unsafe_allow_html=True)


import streamlit as st
import json
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval  # 用于获取星星评分
from supabase import create_client, Client
import uuid

# ✅ Supabase 设置
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ 文本字典（支持中英文）
t_dict = {
    "zh": {
        "title": "📤 上传一瓶你喜欢的酒",
        "wine_name": "酒名",
        "year": "年份",
        "origin": "产地",
        "price": "价格",
        "store": "购买地点",
        "description": "你为什么喜欢这瓶酒？（选填）",
        "photo": "上传酒瓶照片",
        "submit": "提交",
        "warning": "请填写酒名并上传照片！",
        "success": "✅ 上传成功！返回主页查看吧～",
        "back_home": "⬅ 返回首页",
        "rating": "推荐指数",
        "currency": "货币",
        "currency_options": ["人民币 (¥)", "美元 ($)", "欧元 (€)"]
    },
    "en": {
        "title": "📤 Upload Your Favorite Wine",
        "wine_name": "Wine Name",
        "year": "Year",
        "origin": "Origin",
        "price": "Price",
        "store": "Store",
        "description": "Why do you like this wine? (optional)",
        "photo": "Upload Wine Photo",
        "submit": "Submit",
        "warning": "Please fill in wine name and upload photo!",
        "success": "✅ Upload successful! Check it on the home page!",
        "back_home": "⬅ Back to Home",
        "rating": "Rating",
        "currency": "Currency",
        "currency_options": ["CNY (¥)", "USD ($)", "EUR (€)"]
    }
}

# ✅ 根据 URL 参数判断使用中文还是英文
query_params = st.query_params if hasattr(st, 'query_params') else st.experimental_get_query_params()
lang = query_params.get("lang", ["zh"])[0]

# ✅ 根据 lang 选择对应的文本字典（默认为中文）
t = t_dict["en"] if lang == "e" else t_dict["zh"]

# ✅ 页面设置
st.set_page_config(page_title=t["title"], layout="centered")
st.title(t["title"])

# ✅ 显示评分组件
st.markdown(f"### 🌟 {t['rating']}")
components.html("""
<style>
  .star-rating {
    font-size: 36px;
    unicode-bidi: bidi-override;
    direction: ltr;
  }
  .star {
    display: inline-block;
    color: #ccc;
    cursor: pointer;
  }
</style>
<div class="star-rating">
  <span class="star" onclick="setRating(1)">★</span>
  <span class="star" onclick="setRating(2)">★</span>
  <span class="star" onclick="setRating(3)">★</span>
  <span class="star" onclick="setRating(4)">★</span>
  <span class="star" onclick="setRating(5)">★</span>
</div>
<script>
  function setRating(val) {
    localStorage.setItem("rating", val);
    const stars = document.querySelectorAll(".star");
    stars.forEach((star, index) => {
      star.style.color = index < val ? "gold" : "#ccc";
    });
  }
</script>
""", height=50)

# ✅ 获取评分值
rating = streamlit_js_eval(js_expressions="localStorage.getItem('rating')", key="get_rating")
rating_value = int(rating) if rating and rating.isdigit() else 0

# ✅ 上传表单
with st.form("upload_form", clear_on_submit=True):
    wine_name = st.text_input(t["wine_name"])
    year = st.number_input(t["year"], min_value=1900, max_value=datetime.now().year, value=2020)
    origin = st.text_input(t["origin"])

    col1, col2 = st.columns([2, 1])
    with col1:
        price = st.number_input(t["price"], min_value=0.0, step=0.1, key="price_input")
    with col2:
        currency_selection = st.selectbox(t["currency"], t["currency_options"], index=0, key="currency_select")
    currency_symbol = currency_selection.split("(")[-1].replace(")", "")

    store = st.text_input(t["store"])
    description = st.text_area(t["description"], height=100)
    photo = st.file_uploader(t["photo"], type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button(t["submit"])

    if submitted:
        if not wine_name or not photo:
            st.warning(t["warning"])
        else:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{uuid.uuid4().hex}_{photo.name}"
            # 上传图片至 Supabase Storage
            image_path = f"images/{filename}"
            supabase.storage.from_("image").upload(image_path, photo)
            public_url = supabase.storage.from_("image").get_public_url(image_path)

            entry = {
                "wine_name": wine_name,
                "year": int(year),
                "origin": origin,
                "price": float(price),
                "currency": currency_symbol,
                "store": store,
                "description": description,
                "image": public_url,
                "created_at": timestamp,
                "rating": rating_value
            }

            supabase.table("wine_data").insert(entry).execute()

            st.success(t["success"])
            home_url = f"/?lang={lang}"
            st.markdown(f"[🏠 {t['back_home']}]({home_url})", unsafe_allow_html=True)
