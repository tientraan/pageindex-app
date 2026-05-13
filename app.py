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
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS nâng cao
st.markdown("""
    <style>
    /* Nền tổng thể */
    .main { background-color: #f4f6f8; font-family: 'Segoe UI', sans-serif; }
    
    /* Button phong cách web */
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3em; 
        background-color: #007bff; 
        color: white; 
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Input box tròn */
    .stTextInput>div>div>input { 
        border-radius: 10px; 
        height: 2.5em;
        font-size: 16px;
        padding-left: 10px;
    }

    /* Box câu trả lời */
    .answer-box { 
        padding: 20px; 
        background-color: white; 
        border-radius: 15px; 
        border-left: 6px solid #007bff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.5;
    }

    /* Header và footer */
    .title, .caption { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# 2. Header
# ------------------------------
st.markdown("<h1 class='title'>📄 PageIndex Intelligence Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Hệ thống phân tích cấu trúc báo cáo thông minh dựa trên Qwen 2.5</p>", unsafe_allow_html=True)
st.divider()

# ------------------------------
# 3. Hàm xử lý JSON
# ------------------------------
def extract_pageindex_titles(nodes, path=""):
    items = []
    for node in nodes:
        title = node.get('title', '')
        line = node.get('line_num', '')
        current_path = f"{path} > {title}" if path else title
        
        if title and any(keyword in title.lower() for keyword in ["pageindex", "core feature", "quick hands-on", "package usage"]):
            items.append(f"Tiêu đề: {title} (Dòng: {line}) | Đường dẫn: {current_path}")
        
        if 'nodes' in node and node['nodes']:
            items.extend(extract_pageindex_titles(node['nodes'], current_path))
    return items

# ------------------------------
# 4. Load dữ liệu JSON
# ------------------------------
tree_file = Path("data/data_structure.json")
if not tree_file.exists():
    st.error("❌ Không tìm thấy file dữ liệu data_structure.json!")
    st.stop()

with tree_file.open("r", encoding="utf-8") as f:
    data = json.load(f)

all_content = extract_pageindex_titles(data.get('structure', []))

# ------------------------------
# 5. Sidebar chuyên nghiệp
# ------------------------------
st.sidebar.header("🛠 Chức năng nhanh")
st.sidebar.markdown("""
- Nhập câu hỏi về PageIndex.
- Xem các node liên quan.
- Truy xuất Top 30 node làm context.
""")
st.sidebar.markdown("---")
st.sidebar.header("💡 Hướng dẫn sử dụng")
st.sidebar.markdown("""
1. Nhập câu hỏi ở khung chính hoặc chọn câu hỏi mẫu.
2. Bấm " Bắt đầu phân tích".
3. Xem kết quả câu trả lời và các node tham chiếu.
""")

# ------------------------------
# 6. Input câu hỏi & phân tích
# ------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    user_question_input = st.text_input(
        "🔍 Nhập câu hỏi của bạn về PageIndex:", 
        placeholder="Ví dụ: Liệt kê các mục trong Deployment Options..."
    )
    
    if st.button(" Bắt đầu phân tích"):
        if not user_question_input.strip():
            st.warning("⚠️ Vui lòng nhập nội dung câu hỏi!")
        else:
            context_str = "\n".join(all_content[:30])
            full_prompt = f"""Bạn là trợ lý phân tích tài liệu. Dưới đây là cấu trúc báo cáo PageIndex.
            
[DANH SÁCH MỤC LỤC & TIÊU ĐỀ]:
{context_str}

[CÂU HỎI]: {user_question_input}

[YÊU CẦU]: Trả lời chính xác bằng tiếng Việt, trình bày đẹp mắt."""
            
            with st.spinner("🧠 Đang phân tích..."):
                try:
                    response = chat(
                        model="qwen2.5:3b",
                        messages=[{"role": "user", "content": full_prompt}]
                    )
                    
                    answer_text = getattr(response, "text", None) or getattr(response, "message", {}).get("content", "Không lấy được kết quả")
                    
                    st.markdown("### 💡 Kết quả phân tích")
                    st.markdown(f'<div class="answer-box">{answer_text}</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Lỗi khi kết nối Ollama: {str(e)}")

with col_right:
    st.markdown("### 📌 Dữ liệu nguồn")
    with st.expander("Xem chi tiết các Node đã trích xuất", expanded=False):
        if all_content:
            for item in all_content[:30]:
                st.write(f"• {item}")
        else:
            st.write("Không tìm thấy dữ liệu phù hợp.")

# Footer
st.markdown("---")
st.markdown("<center style='color: gray;'>PageIndex Analyzer Tool © 2024</center>", unsafe_allow_html=True)