"""
Page de Prédiction Individuelle
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    FEATURE_GROUPS, ALL_FEATURES, CLASS_LABELS_FR, CLASS_COLORS,
    predict_single, generate_shap_bar
)


def show():
    st.markdown("""
    <h2 style="font-size: 1.6rem; font-weight: 700; color: #1B2A4A; margin-bottom: 6px;">
        Prédiction Individuelle
    </h2>
    <p style="color: #6B7280; font-size: 0.9rem; margin-bottom: 8px;">
        Remplissez les informations de l'étudiant pour obtenir une prédiction avec explication.
    </p>
    <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 20px 0 25px 0;">
    """, unsafe_allow_html=True)

    input_values = {}
    st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 14px;">Informations de l\'étudiant</h3>', unsafe_allow_html=True)
    
    for group_name, features in FEATURE_GROUPS.items():
        with st.expander(group_name, expanded=(group_name in ["Informations Personnelles", "Situation Financière"])):
            feature_items = list(features.items())
            for i in range(0, len(feature_items), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(feature_items):
                        feat_name, feat_config = feature_items[i + j]
                        with cols[j]:
                            if feat_config["type"] == "select":
                                options = feat_config["options"]
                                display_options = list(options.values())
                                selected_label = st.selectbox(feat_config["label"], display_options, key=f"sel_{feat_name}")
                                reverse_map = {v: k for k, v in options.items()}
                                input_values[feat_name] = reverse_map[selected_label]
                            elif feat_config["type"] == "slider":
                                val = st.slider(feat_config["label"], min_value=feat_config["min"],
                                    max_value=feat_config["max"], value=feat_config["default"],
                                    step=feat_config.get("step", 1), key=f"sld_{feat_name}")
                                input_values[feat_name] = val

    col_btn1, col_btn2, col_btn3 = st.columns([1, 0.6, 1])
    with col_btn2:
        predict_clicked = st.button("Lancer la prédiction", use_container_width=True)

    if predict_clicked:
        st.markdown('<hr style="border: none; border-top: 1px solid #E5E7EB; margin: 25px 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 15px;">Résultat de la prédiction</h3>', unsafe_allow_html=True)
        
        with st.spinner("Analyse en cours..."):
            try:
                class_idx, class_label, probas = predict_single(input_values)
                css_class = {0: "dropout", 1: "enrolled", 2: "graduate"}[class_idx]
                if class_idx == 0:
                    alert_msg = "Cet étudiant présente un risque élevé d'abandon."
                elif class_idx == 1:
                    alert_msg = "Cet étudiant est inscrit mais n'est pas encore diplômé."
                else:
                    alert_msg = "Cet étudiant est en voie d'obtention de diplôme."
                
                st.markdown(f"""
                <div class="result-card {css_class}">
                    <div class="result-label">Prédiction</div>
                    <div class="result-value {css_class}">{class_label.upper()}</div>
                    <div class="result-alert">{alert_msg}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<h4 style="font-size: 0.95rem; font-weight: 600; color: #1B2A4A; margin: 20px 0 10px 0;">Probabilités par classe</h4>', unsafe_allow_html=True)
                color_map = {"Abandon": "red", "Inscrit": "orange", "Diplômé": "green"}
                value_color_map = {"Abandon": "#DC2626", "Inscrit": "#D97706", "Diplômé": "#16A34A"}
                for label, prob in probas.items():
                    bar_color = color_map[label]
                    text_color = value_color_map[label]
                    st.markdown(f"""
                    <div class="prob-row">
                        <div class="prob-header">
                            <span class="prob-label">{label}</span>
                            <span class="prob-value" style="color: {text_color};">{prob*100:.1f}%</span>
                        </div>
                        <div class="prob-bar-bg">
                            <div class="prob-bar {bar_color}" style="width: {prob*100}%"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                dropout_prob = probas.get("Abandon", 0)
                if dropout_prob >= 0.6:
                    risk_level, risk_css = "RISQUE CRITIQUE", "critique"
                elif dropout_prob >= 0.4:
                    risk_level, risk_css = "RISQUE ÉLEVÉ", "eleve"
                elif dropout_prob >= 0.2:
                    risk_level, risk_css = "RISQUE MOYEN", "moyen"
                else:
                    risk_level, risk_css = "RISQUE FAIBLE", "faible"
                st.markdown(f"""
                <div class="risk-box {risk_css}">
                    <span class="risk-level {risk_css}">{risk_level}</span>
                    <span class="risk-detail">Probabilité d'abandon : {dropout_prob*100:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<h4 style="font-size: 0.95rem; font-weight: 600; color: #1B2A4A; margin: 20px 0 8px 0;">Explication des facteurs (SHAP)</h4>', unsafe_allow_html=True)
                st.markdown('<p style="color: #9CA3AF; font-size: 0.8rem; margin-bottom: 12px;">Les facteurs en vert augmentent la probabilité de la classe prédite, ceux en rouge la diminuent.</p>', unsafe_allow_html=True)
                try:
                    fig_shap = generate_shap_bar(input_values)
                    if fig_shap is not None:
                        st.pyplot(fig_shap)
                    else:
                        st.info("Explication SHAP non disponible (explicateur non chargé)")
                except Exception as e:
                    st.warning(f"Impossible de générer l'explication SHAP : {str(e)}")
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {str(e)}")
                st.info("Vérifiez que les fichiers du modèle sont bien dans le dossier models/")
