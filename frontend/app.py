import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Auto Job Apply",
    layout="centered"
)

st.title("🚀 Auto Job Apply")
st.caption("AI-powered Resume Parsing & Job Matching")

st.divider()

# ----------------------------
# USER ID INPUT
# ----------------------------
user_id = st.number_input(
    "Enter User ID",
    min_value=1,
    step=1
)

# ----------------------------
# RESUME UPLOAD
# ----------------------------
st.subheader("📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

if uploaded_file and user_id:
    if st.button("Upload Resume"):
        with st.spinner("Uploading & extracting skills..."):
            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }
            response = requests.post(
                f"{API_BASE}/resume/upload/{user_id}",
                files=files
            )

        if response.status_code == 200:
            data = response.json()

            st.success("Resume uploaded successfully 🎉")

            st.markdown("### ✅ Extracted Skills")
            st.write(", ".join(data["extracted_skills"]))

            st.info(f"Total skills detected: {data['skill_count']}")
        else:
            st.error("Resume upload failed ❌")

st.divider()