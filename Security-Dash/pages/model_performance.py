# pages/3_📈_Model_Performance.py
import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix
import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")
st.title("📈 Model Performance Evaluation")

# --- Paths ---
MODEL_PATH = os.path.join("data", "stage1_binary_pipeline_A.joblib")
FEATURE_IMPORTANCE_PATH = os.path.join("data", "feature_importance_stage1.png") 

# --- Check if model exists ---
if not os.path.exists(MODEL_PATH):
    st.warning("Model not found. Please add it to /data folder to display results.")
    st.stop()

# --- Load model ---
model = joblib.load(MODEL_PATH)

# --- Pipeline Overview ---
st.subheader("🔹 Pipeline Overview")
with st.expander("View Pipeline Steps"):
    for step_name, step_obj in model.named_steps.items():
        st.markdown(f"**{step_name}:**")
        st.code(str(step_obj), language="python")

# --- Simulated Evaluation (replace with real test set if available) ---
st.subheader("🔹 Model Metrics")

# Dummy evaluation
y_true = [0, 0, 1, 1, 0, 1, 1, 0]
y_pred = [0, 1, 1, 1, 0, 1, 0, 0]

# Classification report
report_dict = classification_report(y_true, y_pred, target_names=["BENIGN", "ATTACK"], output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()

st.markdown("**Classification Report**")
st.dataframe(report_df.style.format("{:.2f}"))

# Confusion matrix
st.markdown("**Confusion Matrix**")
cm = confusion_matrix(y_true, y_pred)
fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=["Pred BENIGN", "Pred ATTACK"],
    y=["True BENIGN", "True ATTACK"],
    colorscale="Blues",
    showscale=True
)
fig_cm.update_layout(title_text="Confusion Matrix", title_x=0.5)
st.plotly_chart(fig_cm, use_container_width=True)

# --- Feature Importance ---
st.subheader("🔹 Feature Importance (Top Features)")
if os.path.exists(FEATURE_IMPORTANCE_PATH):
    img = Image.open(FEATURE_IMPORTANCE_PATH)
    st.image(img, use_container_width=True)
else:
    st.warning("Feature importance plot not found. You can generate it using 'model2.ipynb'.")

