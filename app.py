import streamlit as st
import json
from pathlib import Path
import re

# Load dữ liệu JSON
tree_file = Path("data/data_structure.json")
with tree_file.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Hàm traverse JSON và tìm node liên quan
def search_nodes(node, keyword, path=""):
    results = []
    if isinstance(node, dict):
        title = node.get("title","")
        text = node.get("text","")
        new_path = f"{path} > {title}" if title else path
        combined = f"{title} {text}".lower()
        if keyword.lower() in combined:
            results.append({"path": new_path, "text": combined})
        for child in node.get("nodes", []):
            results.extend(search_nodes(child, keyword, new_path))
    elif isinstance(node, list):
        for item in node:
            results.extend(search_nodes(item, keyword, path))
    return results

# Streamlit UI
st.title("PageIndex Search Tool")
query = st.text_input("Nhập từ khóa tìm kiếm:")
if st.button("Tìm kiếm"):
    if query.strip():
        matched = search_nodes(data.get("structure", []), query.strip())
        if matched:
            st.write(f"Tìm thấy {len(matched)} node:")
            for m in matched:
                st.markdown(f"**{m['path']}**")
                st.code(m['text'])
        else:
            st.info("Không tìm thấy node liên quan.")