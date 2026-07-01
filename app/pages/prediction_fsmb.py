"""
Page Adaptation FSBM - Modele entraine sur les donnees marocaines
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils_fsmb import (
    FEATURE_DEFS, ALL_FEATURES, CLASS_LABELS_FR, CLASS_COLORS,
    predict_single, generate_shap_bar
)


def show():
    st.markdown("""
    <h2 style="font-size: 1.6rem; font-weight: 700; color: #1B2A4A; margin-bottom: 6px;">
        Prediction FSBM - Adaptation Marocaine
    </h2>
    <p style="color: #6B7280; font-size: 0.9rem; margin-bottom: 4px;">
        Modele entraine sur les donnees FSBM (6009 etudiants, 6 features). Prediction binaire : Abandon / Reinscription.
    </p>
    <div style="background: #FFF7ED; border: 1px solid #FDBA74; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.82rem; color: #92400E;">
        Modele proof-of-concept avec 6 features. Precision : 84.5%. Les performances seront ameliorees avec davantage de features collectees aupres de l'administration.
    </div>
    <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 15px 0 20px 0;">
    """, unsafe_allow_html=True)

    input_values = {}

    # Informations Academiques
    st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 12px;">Informations Academiques</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        feat = FEATURE_DEFS["Filiere_code"]
        options = feat["options"]
        display_options = list(options.values())
        selected_label = st.selectbox(feat["label"], display_options, key="sel_filiere")
        reverse_map = {v: k for k, v in options.items()}
        input_values["Filiere_code"] = reverse_map[selected_label]

        feat = FEATURE_DEFS["Bac_code"]
        options = feat["options"]
        display_options = list(options.values())
        selected_label = st.selectbox(feat["label"], display_options, key="sel_bac")
        reverse_map = {v: k for k, v in options.items()}
        input_values["Bac_code"] = reverse_map[selected_label]

    with col2:
        feat = FEATURE_DEFS["Mention_code"]
        options = feat["options"]
        display_options = list(options.values())
        selected_label = st.selectbox(feat["label"], display_options, key="sel_mention")
        reverse_map = {v: k for k, v in options.items()}
        input_values["Mention_code"] = reverse_map[selected_label]

        feat = FEATURE_DEFS["Age_inscription"]
        val = st.slider(feat["label"], min_value=feat["min"],
            max_value=feat["max"], value=feat["default"],
            step=feat.get("step", 1), key="sld_age")
        input_values["Age_inscription"] = val

    # Resultats Academiques
    st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin: 20px 0 12px 0;">Resultats Academiques</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        feat = FEATURE_DEFS["SEMESTRE 1"]
        val = st.slider(feat["label"], min_value=feat["min"],
            max_value=feat["max"], value=feat["default"],
            step=feat.get("step", 0.25), key="sld_s1")
        input_values["SEMESTRE 1"] = val

    with col2:
        feat = FEATURE_DEFS["SEMESTRE 2"]
        val = st.slider(feat["label"], min_value=feat["min"],
            max_value=feat["max"], value=feat["default"],
            step=feat.get("step", 0.25), key="sld_s2")
        input_values["SEMESTRE 2"] = val

    # Bouton Prediction
    col_btn1, col_btn2, col_btn3 = st.columns([1, 0.6, 1])
    with col_btn2:
        predict_clicked = st.button("Lancer la prediction", use_container_width=True)

    if predict_clicked:
        st.markdown('<hr style="border: none; border-top: 1px solid #E5E7EB; margin: 25px 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 15px;">Resultat de la prediction</h3>', unsafe_allow_html=True)

        with st.spinner("Analyse en cours..."):
            try:
                class_idx, class_label, probas = predict_single(input_values)
                css_class = "dropout" if class_idx == 1 else "reinscrit"
                if class_idx == 1:
                    alert_msg = "Cet etudiant presente un risque eleve d'abandon."
                else:
                    alert_msg = "Cet etudiant est susceptible de se reinscrire."

                st.markdown(f"""
                <div class="result-card {css_class}">
                    <div class="result-label">Prediction</div>
                    <div class="result-value {css_class}">{class_label.upper()}</div>
                    <div class="result-alert">{alert_msg}</div>
                </div>
                """, unsafe_allow_html=True)

                # Probabilites
                st.markdown('<h4 style="font-size: 0.95rem; font-weight: 600; color: #1B2A4A; margin: 20px 0 10px 0;">Probabilites</h4>', unsafe_allow_html=True)
                color_map = {"Reinscrit": "green", "Abandonne": "red"}
                value_color_map = {"Reinscrit": "#16A34A", "Abandonne": "#DC2626"}
                for label, prob in probas.items():
                    bar_color = color_map.get(label, "green")
                    text_color = value_color_map.get(label, "#16A34A")
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

                # Niveau de risque
                abandon_prob = probas.get("Abandonne", 0)
                if abandon_prob >= 0.6:
                    risk_level, risk_css = "RISQUE CRITIQUE", "critique"
                elif abandon_prob >= 0.4:
                    risk_level, risk_css = "RISQUE ELEVE", "eleve"
                elif abandon_prob >= 0.2:
                    risk_level, risk_css = "RISQUE MOYEN", "moyen"
                else:
                    risk_level, risk_css = "RISQUE FAIBLE", "faible"
                st.markdown(f"""
                <div class="risk-box {risk_css}">
                    <span class="risk-level {risk_css}">{risk_level}</span>
                    <span class="risk-detail">Probabilite d'abandon : {abandon_prob*100:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)

                # SHAP
                st.markdown('<h4 style="font-size: 0.95rem; font-weight: 600; color: #1B2A4A; margin: 20px 0 8px 0;">Facteurs explicatifs (SHAP)</h4>', unsafe_allow_html=True)
                st.markdown('<p style="color: #9CA3AF; font-size: 0.8rem; margin-bottom: 12px;">Les facteurs en vert favorisent la classe predite, ceux en rouge la defavorisent.</p>', unsafe_allow_html=True)
                try:
                    fig_shap = generate_shap_bar(input_values)
                    if fig_shap is not None:
                        st.pyplot(fig_shap)
                    else:
                        st.info("Explication SHAP non disponible (explicateur non charge)")
                except Exception as e:
                    st.warning(f"Impossible de generer l'explication SHAP : {str(e)}")

            except Exception as e:
                st.error(f"Erreur lors de la prediction : {str(e)}")
                st.info("Verifiez que les fichiers du modele sont bien dans le dossier models_fsmb/")
