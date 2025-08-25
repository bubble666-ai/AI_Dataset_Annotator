import streamlit as st
import pandas as pd
import os
from PIL import Image
import time

# --- Initial Setup and Data Loading ---
st.set_page_config(layout="wide", page_title="Smart Labeling Tool")

# File paths
DATASET_PATH = os.path.join('..', 'data', 'final_dataset_with_confidence.csv') # <--- Changed
VERIFIED_PATH = os.path.join('..', 'data', 'verified_labels.csv')

@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"Dataset file not found at {path}. Please run the notebook first to generate confidence scores.")
        return None
    return pd.read_csv(path)

df = load_data(DATASET_PATH)

if df is None:
    st.stop()

# --- State Management and Active Learning Logic ---

if os.path.exists(VERIFIED_PATH):
    verified_df = pd.read_csv(VERIFIED_PATH, index_col=0)
else:
    verified_df = pd.DataFrame(columns=df.columns.tolist() + ['verified_label', 'status'])

# Unverified dataframe includes all rows that have not yet been reviewed
unverified_df = df.drop(index=verified_df.index, errors='ignore')

if unverified_df.empty:
    st.success("🎉 Congratulations! All images have been reviewed.")
    st.balloons()
    st.stop()

# --- Core of Active Learning ---
# Instead of random selection, choose the row with the lowest confidence score
st.session_state.current_index = unverified_df['confidence'].idxmin()

# (The save_verification and go_to_next_image functions remain unchanged, but go_to_next_image is no longer needed)
def save_verification(index, original_row, verified_label, status):
    new_row = original_row.copy()
    new_row['verified_label'] = verified_label
    new_row['status'] = status
    new_df_row = pd.DataFrame([new_row], index=[index])
    
    if os.path.exists(VERIFIED_PATH):
        current_verified_df = pd.read_csv(VERIFIED_PATH, index_col=0)
        updated_df = pd.concat([current_verified_df, new_df_row])
    else:
        updated_df = new_df_row
        
    updated_df.to_csv(VERIFIED_PATH, index=True)

# --- User Interface ---
st.title("🔍 Active Learning Labeling Tool")

# ... (Progress statistics section unchanged) ...
st.write(f"**Total Images:** {len(df)}")
st.write(f"**Reviewed:** {len(verified_df)}")
st.write(f"**Remaining:** {len(unverified_df)}")
progress_value = len(verified_df) / len(df)
st.progress(progress_value)

st.markdown("---")

current_idx = st.session_state.current_index
original_row = df.loc[current_idx]
image_path = original_row['filepath']
weak_label = original_row['weak_label']
confidence = original_row['confidence']

col_img, col_info = st.columns([2, 1])

with col_img:
    image = Image.open(image_path)
    st.image(image, use_container_width=True)

with col_info:
    st.write(f"**True Label (for testing):** `{original_row['ground_truth']}`")
    st.subheader(f"AI Suggested Label: `{weak_label}`")
    
    # Display confidence score
    st.metric(label="AI Confidence Score", value=f"{confidence:.2%}")
    if confidence < 0.6:
        st.warning("The AI has low confidence in this label!")
    else:
        st.info("The AI is relatively confident in this label.")

    categories = sorted(df['ground_truth'].unique().tolist())
    if weak_label not in categories:
        categories.append(weak_label)
    try:
        default_index = categories.index(weak_label)
    except ValueError:
        default_index = 0

    corrected_label = st.selectbox(
        "If the label is incorrect, select the correct one:",
        options=categories,
        index=default_index
    )

    if st.button("✅ Confirm and Save", type="primary", use_container_width=True):
        save_verification(current_idx, original_row, corrected_label, "verified")
        st.success(f"Label '{corrected_label}' saved.")
        time.sleep(0.5)
        st.rerun()

    if st.button("⏭️ Skip", use_container_width=True):
        save_verification(current_idx, original_row, None, "skipped")
        st.info("This image was skipped.")
        time.sleep(0.5)
        st.rerun()