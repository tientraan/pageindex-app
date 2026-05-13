import streamlit as st

import json

from pathlib import Path

import re

from ollama import chat

# ------------------------------

# 1. Cấu hình trang

# ------------------------------

st.set_page_config(
    page_title="PageIndex Intelligence Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS nâng cao cho giao diện chuyên nghiệp

st.markdown(
    """

    <style>

    /* Nền tổng thể */

    .main { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }

   

    /* Button phong cách hiện đại */

    .stButton>button {

        width: 100%;

        border-radius: 12px;

        height: 3.2em;

        background: linear-gradient(90deg, #4285F4, #34A853);

        color: white;

        font-weight: 600;

        font-size: 16px;

        border: none;

        transition: 0.3s;

    }

    .stButton>button:hover {

        opacity: 0.9;

        box-shadow: 0 4px 12px rgba(0,0,0,0.15);

    }

   

    /* Input box */

    .stTextInput>div>div>input {

        border-radius: 10px;

        height: 2.8em;

        font-size: 16px;

    }



    /* Box câu trả lời phong cách Google Gemma */

    .answer-box {

        padding: 25px;

        background-color: white;

        border-radius: 15px;

        border-left: 8px solid #4285F4;

        box-shadow: 0 10px 25px rgba(0,0,0,0.05);

        font-size: 17px;

        line-height: 1.6;

        color: #333;

    }



    /* Sidebar Styling */

    section[data-testid="stSidebar"] {

        background-color: #ffffff;

        border-right: 1px solid #e0e0e0;

    }

    </style>

""",
    unsafe_allow_html=True,
)


# ------------------------------

# 2. Header

# ------------------------------

st.markdown(
    "<h1 style='text-align: center; color: #1A73E8;'> PageIndex Intelligence Analyzer</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align: center; color: #5f6368; font-size: 1.1em;'>Hệ thống phân tích cấu trúc báo cáo dựa trên <b>Google Gemma 2 2B</b></p>",
    unsafe_allow_html=True,
)

st.divider()


# ------------------------------

# 3. Hàm xử lý dữ liệu

# ------------------------------


def extract_pageindex_titles(nodes, path=""):

    items = []

    for node in nodes:

        title = node.get("title", "")

        line = node.get("line_num", "")

        current_path = f"{path} > {title}" if path else title

        # Lọc các từ khóa quan trọng

        keywords = [
            "pageindex",
            "core feature",
            "quick hands-on",
            "package usage",
            "deployment",
            "configuration",
        ]

        if title and any(keyword in title.lower() for keyword in keywords):

            items.append(f"Tiêu đề: {title} (Dòng: {line}) | Đường dẫn: {current_path}")

        if "nodes" in node and node["nodes"]:

            items.extend(extract_pageindex_titles(node["nodes"], current_path))

    return items


# ------------------------------

# 4. Tải dữ liệu JSON

# ------------------------------

tree_file = Path("data/data_structure.json")


if not tree_file.exists():

    st.error(
        "❌ Không tìm thấy file 'data/data_structure.json'. Vui lòng kiểm tra lại thư mục!"
    )

    st.stop()


try:

    with tree_file.open("r", encoding="utf-8") as f:

        data = json.load(f)

    all_content = extract_pageindex_titles(data.get("structure", []))

except Exception as e:

    st.error(f"❌ Lỗi khi đọc file JSON: {e}")

    st.stop()


# ------------------------------

# 5. Sidebar (ĐÃ CẬP NHẬT THÔNG TIN MODEL)

# ------------------------------

with st.sidebar:

    st.image(
        "https://www.gstatic.com/lamda/images/favicon_v2_6efed324545161ba.png", width=50
    )

    st.header("Cấu hình AI")

    # Đã đổi thông tin hiển thị thành bản 2B

    st.info(
        "Model: **Gemma 2 2B**\n\nĐây là phiên bản gọn nhẹ, tối ưu bộ nhớ nhưng vẫn cực kỳ mạnh mẽ trong việc phân tích văn bản."
    )

    st.markdown("---")

    st.subheader("💡 Gợi ý câu hỏi")

    st.caption("- Tổng quan về PageIndex là gì?")

    st.caption("- Các bước trong Deployment Options?")

    st.caption("- Tìm các mục liên quan đến Package Usage.")


# ------------------------------

# 6. Giao diện chính & Xử lý AI

# ------------------------------

col_main, col_info = st.columns([2, 1])


with col_main:

    user_question = st.text_input(
        "🔍 Bạn muốn tìm hiểu gì về cấu trúc PageIndex?",
        placeholder="Nhập nội dung câu hỏi tại đây...",
    )

    if st.button("🚀 Bắt đầu phân tích"):

        if not user_question.strip():

            st.warning("⚠️ Vui lòng nhập câu hỏi để Gemma có thể hỗ trợ bạn!")

        else:

            context_str = "\n".join(all_content[:35])

            prompt = f"""Bạn là một chuyên gia phân tích tài liệu kỹ thuật.

Hãy sử dụng thông tin cấu trúc dưới đây để trả lời câu hỏi của người dùng.



[DỮ LIỆU CẤU TRÚC BÁO CÁO]:

{context_str}



[CÂU HỎI]: {user_question}



[YÊU CẦU]:

- Trả lời bằng tiếng Việt chuyên nghiệp.

- Nếu thông tin có trong cấu trúc, hãy chỉ rõ tiêu đề và vị trí dòng.

- Sử dụng bullet points để thông tin rõ ràng.

- Nếu không thấy thông tin trong dữ liệu, hãy dựa vào kiến thức chung về PageIndex để gợi ý."""

            # Đã đổi thông báo spinner thành bản 2B

            with st.spinner("🤖 Gemma 2 (2B) đang phân tích dữ liệu..."):

                try:

                    # QUAN TRỌNG: Đã đổi model="gemma2:9b" thành model="gemma2:2b"

                    response = chat(
                        model="gemma2:2b",
                        messages=[{"role": "user", "content": prompt}],
                    )

                    content = response["message"]["content"]

                    st.markdown("### 💡 Kết quả phân tích từ Gemma")

                    st.markdown(
                        f'<div class="answer-box">{content}</div>',
                        unsafe_allow_html=True,
                    )

                except Exception as e:

                    st.error(f"❌ Lỗi kết nối Ollama: {str(e)}")

                    st.info(
                        "Kiểm tra xem bạn đã chạy lệnh: `ollama run gemma2:2b` chưa."
                    )


with col_info:

    st.markdown("### 📌 Metadata")

    st.write(f"Tổng số Node trích xuất: **{len(all_content)}**")

    with st.expander("Danh sách Node tham chiếu", expanded=True):

        if all_content:

            for item in all_content[:20]:

                st.caption(f"• {item}")

        else:

            st.write("Dữ liệu trống.")


# Footer

st.markdown("---")

st.markdown(
    "<center style='color: #80868b; font-size: 0.9em;'>Powered by Google Gemma 2 (2B) & Ollama • 2024</center>",
    unsafe_allow_html=True,
)
