"""
Shared utilities for the FSBM (Moroccan) model
Model loading, prediction, SHAP, feature definitions
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# ========== PATHS ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models_fsmb")

# ========== FEATURE DEFINITIONS ==========
FEATURE_DEFS = {
    "Filiere_code": {
        "type": "select",
        "label": "Filiere FSBM",
        "options": {
            0: "MIP",
            1: "BCG",
            2: "Informatique Appliquee",
            3: "Physique Chimie"
        }
    },
    "Bac_code": {
        "type": "select",
        "label": "Filiere Bac",
        "options": {
            0: "Sciences Mathematiques A",
            1: "Sciences Mathematiques B",
            2: "Sciences Physiques",
            3: "Sciences de la Vie et de la Terre",
            4: "Sciences Economiques",
            5: "Lettres"
        }
    },
    "Mention_code": {
        "type": "select",
        "label": "Mention Bac",
        "options": {
            0: "Passable",
            1: "Assez Bien",
            2: "Bien",
            3: "Tres Bien"
        }
    },
    "SEMESTRE 1": {
        "type": "slider",
        "label": "Moyenne Semestre 1",
        "min": 0.0,
        "max": 20.0,
        "default": 10.0,
        "step": 0.25
    },
    "SEMESTRE 2": {
        "type": "slider",
        "label": "Moyenne Semestre 2",
        "min": 0.0,
        "max": 20.0,
        "default": 10.0,
        "step": 0.25
    },
    "Age_inscription": {
        "type": "slider",
        "label": "Age a l'inscription",
        "min": 15,
        "max": 45,
        "default": 19,
        "step": 1
    }
}

ALL_FEATURES = ['Filiere_code', 'Bac_code', 'Mention_code', 'SEMESTRE 1', 'SEMESTRE 2', 'Age_inscription']

CLASS_NAMES = {0: "Reinscrit", 1: "Abandonne"}
CLASS_LABELS_FR = {0: "Reinscrit", 1: "Abandonne"}
CLASS_COLORS = {0: "#16A34A", 1: "#DC2626"}

# ========== MODEL LOADING ==========
@st.cache_resource
def load_model():
    pkl_path = os.path.join(MODELS_DIR, "model_fsmb.pkl")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement du modele FSBM : {e}")
        st.stop()

@st.cache_resource
def load_scaler():
    pkl_path = os.path.join(MODELS_DIR, "scaler_fsmb.pkl")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement du scaler FSBM : {e}")
        st.stop()

@st.cache_resource
def load_encoders():
    pkl_path = os.path.join(MODELS_DIR, "encoders_fsmb.pkl")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement des encodeurs FSBM : {e}")
        st.stop()

@st.cache_resource
def load_shap_explainer():
    pkl_path = os.path.join(MODELS_DIR, "shap_explainer_fsmb.pkl")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.warning(f"Impossible de charger l'explicateur SHAP FSBM : {e}")
        return None

# ========== PREDICTION ==========
def predict_single(input_dict):
    model = load_model()
    scaler = load_scaler()
    df = pd.DataFrame([input_dict])
    df = df[ALL_FEATURES]
    X_scaled = scaler.transform(df)
    class_idx = int(model.predict(X_scaled)[0])
    probas = model.predict_proba(X_scaled)[0]
    proba_dict = {}
    for i, name in CLASS_NAMES.items():
        proba_dict[CLASS_LABELS_FR[i]] = float(probas[i])
    return class_idx, CLASS_LABELS_FR[class_idx], proba_dict

def predict_batch(df_input):
    model = load_model()
    scaler = load_scaler()
    for col in ALL_FEATURES:
        if col not in df_input.columns:
            df_input[col] = 0
    df_ordered = df_input[ALL_FEATURES]
    X_scaled = scaler.transform(df_ordered)
    predictions = model.predict(X_scaled)
    probas = model.predict_proba(X_scaled)
    result_df = df_input.copy()
    result_df["Prediction"] = [CLASS_LABELS_FR[int(p)] for p in predictions]
    result_df["Prob_Abandonne"] = [float(p[1]) for p in probas]
    result_df["Prob_Reinscrit"] = [float(p[0]) for p in probas]
    return result_df

# ========== SHAP ==========
def generate_shap_bar(input_dict):
    model = load_model()
    scaler = load_scaler()
    explainer = load_shap_explainer()
    if explainer is None:
        return None
    df = pd.DataFrame([input_dict])
    df = df[ALL_FEATURES]
    X_scaled = scaler.transform(df)
    shap_values = explainer.shap_values(X_scaled)
    class_idx = int(model.predict(X_scaled)[0])

    if isinstance(shap_values, list):
        class_shap = shap_values[class_idx][0]
    elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        class_shap = shap_values[0, :, class_idx]
    else:
        class_shap = shap_values[0]

    class_shap_flat = np.array([float(v) for v in class_shap])
    feature_importance = list(zip(ALL_FEATURES, class_shap_flat))
    feature_importance.sort(key=lambda x: abs(float(x[1])), reverse=True)
    top_features = feature_importance[:6]
    top_features.reverse()
    names = [f[0] for f in top_features]
    values = [float(f[1]) for f in top_features]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    colors = ['#DC2626' if v < 0 else '#16A34A' for v in values]
    ax.barh(range(len(names)), values, color=colors, height=0.6, edgecolor='none')
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9, color='#374151')
    ax.tick_params(axis='x', colors='#9CA3AF')
    ax.set_xlabel('Impact SHAP', color='#6B7280', fontsize=11)
    class_label = CLASS_LABELS_FR[class_idx]
    ax.set_title(f'Explication SHAP - {class_label}', color='#1B2A4A', fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='x', alpha=0.15, color='#9CA3AF')
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color('#E5E7EB')
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#16A34A', label='Favorise la classe predite'),
        Patch(facecolor='#DC2626', label='Defavorise la classe predite')
    ]
    ax.legend(handles=legend_elements, loc='lower right',
              facecolor='#F9FAFB', edgecolor='#E5E7EB',
              labelcolor='#374151', fontsize=9)
    plt.tight_layout()
    return fig
