"""
Page de Prédiction Batch
"""
import streamlit as st
import pandas as pd
import sys
import os
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    ALL_FEATURES, CLASS_LABELS_FR,
    predict_batch, get_csv_template, validate_csv
)


def show():
    st.markdown("""
    <h2 style="font-size: 1.6rem; font-weight: 700; color: #1B2A4A; margin-bottom: 6px;">
        Prédiction Batch
    </h2>
    <p style="color: #6B7280; font-size: 0.9rem; margin-bottom: 8px;">
        Importez un fichier CSV contenant les données de plusieurs étudiants pour obtenir des prédictions en masse.
    </p>
    <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 20px 0 25px 0;">
    """, unsafe_allow_html=True)

    st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 10px;">Étape 1 : Préparer le fichier</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6B7280; font-size: 0.85rem; margin-bottom: 14px; line-height: 1.5;">Téléchargez le modèle CSV et remplissez-le avec les données de vos étudiants. Le fichier doit contenir les 36 colonnes du modèle.</p>', unsafe_allow_html=True)
    
    sample_row = {
        'Marital Status': 1, 'Application mode': 1, 'Application order': 1, 'Course': 9130,
        'Daytime/evening attendance': 1, 'Previous qualification': 1,
        'Previous qualification (grade)': 130.0, 'Nacionality': 1,
        "Mother's qualification": 1, "Father's qualification": 1,
        "Mother's occupation": 2, "Father's occupation": 2,
        'Admission grade': 125.0, 'Displaced': 0, 'Educational special needs': 0,
        'Debtor': 0, 'Tuition fees up to date': 1, 'Gender': 1,
        'Scholarship holder': 0, 'Age at enrollment': 20, 'International': 0,
        'Curricular units 1st sem (credited)': 0, 'Curricular units 1st sem (enrolled)': 6,
        'Curricular units 1st sem (evaluations)': 8, 'Curricular units 1st sem (approved)': 5,
        'Curricular units 1st sem (grade)': 10.5, 'Curricular units 1st sem (without evaluations)': 0,
        'Curricular units 2nd sem (credited)': 0, 'Curricular units 2nd sem (enrolled)': 6,
        'Curricular units 2nd sem (evaluations)': 8, 'Curricular units 2nd sem (approved)': 4,
        'Curricular units 2nd sem (grade)': 10.0, 'Curricular units 2nd sem (without evaluations)': 0,
        'Unemployment rate': 11.6, 'Inflation rate': 1.2, 'GDP': 0.0
    }
    template_df = pd.DataFrame([sample_row])
    csv_buffer = io.StringIO()
    template_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    col_dl1, col_dl2, col_dl3 = st.columns([1, 0.5, 1])
    with col_dl2:
        st.download_button(label="Télécharger le modèle CSV", data=csv_data,
            file_name="template_etudiants.csv", mime="text/csv")
    
    st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin: 25px 0 10px 0;">Étape 2 : Importer le fichier</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sélectionnez votre fichier CSV", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            st.success(f"Fichier chargé : **{len(df_uploaded)}** étudiants détectés")
            is_valid, msg, df_clean = validate_csv(df_uploaded.copy())
            if not is_valid:
                st.warning(msg)
                st.info("Les colonnes manquantes seront remplies avec des valeurs par défaut.")
            
            with st.expander("Aperçu des données importées"):
                st.dataframe(df_uploaded.head(10), height=300)
                st.caption(f"Affichage des 10 premières lignes sur {len(df_uploaded)}")
            
            col_p1, col_p2, col_p3 = st.columns([1, 0.5, 1])
            with col_p2:
                batch_predict = st.button("Lancer les prédictions", use_container_width=True)
            
            if batch_predict:
                with st.spinner(f"Analyse de {len(df_clean)} étudiants en cours..."):
                    try:
                        results_df = predict_batch(df_clean)
                        st.markdown('<hr style="border: none; border-top: 1px solid #E5E7EB; margin: 25px 0;">', unsafe_allow_html=True)
                        st.markdown('<h3 style="font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 15px;">Résultats</h3>', unsafe_allow_html=True)
                        
                        pred_counts = results_df["Prédiction"].value_counts()
                        total = len(results_df)
                        n_dropout = pred_counts.get("Abandon", 0)
                        n_enrolled = pred_counts.get("Inscrit", 0)
                        n_graduate = pred_counts.get("Diplômé", 0)
                        
                        sum_cols = st.columns(4)
                        with sum_cols[0]:
                            st.markdown(f'<div class="summary-card"><div class="summary-number blue">{total}</div><div class="summary-label">Total étudiants</div></div>', unsafe_allow_html=True)
                        with sum_cols[1]:
                            st.markdown(f'<div class="summary-card"><div class="summary-number red">{n_dropout}</div><div class="summary-label">Abandon</div></div>', unsafe_allow_html=True)
                        with sum_cols[2]:
                            st.markdown(f'<div class="summary-card"><div class="summary-number orange">{n_enrolled}</div><div class="summary-label">Inscrit</div></div>', unsafe_allow_html=True)
                        with sum_cols[3]:
                            st.markdown(f'<div class="summary-card"><div class="summary-number green">{n_graduate}</div><div class="summary-label">Diplômé</div></div>', unsafe_allow_html=True)
                        
                        high_risk = results_df[results_df["Prob_Abandon"] >= 0.5]
                        if len(high_risk) > 0:
                            st.markdown(f'<div class="alert-box">{len(high_risk)} étudiant(s) avec une probabilité d\'abandon supérieure ou égale à 50%</div>', unsafe_allow_html=True)
                        
                        st.markdown('<h4 style="font-size: 0.95rem; font-weight: 600; color: #1B2A4A; margin: 20px 0 10px 0;">Détail des prédictions</h4>', unsafe_allow_html=True)
                        display_cols = ["Prédiction", "Prob_Abandon", "Prob_Inscrit", "Prob_Diplômé"]
                        orig_cols = [c for c in results_df.columns if c not in display_cols]
                        show_df = results_df[orig_cols + display_cols].copy()
                        for col in ["Prob_Abandon", "Prob_Inscrit", "Prob_Diplômé"]:
                            if col in show_df.columns:
                                show_df[col] = show_df[col].apply(lambda x: f"{x*100:.1f}%")
                        st.dataframe(show_df, height=400)
                        
                        result_csv = results_df.to_csv(index=False)
                        col_d1, col_d2, col_d3 = st.columns([1, 0.5, 1])
                        with col_d2:
                            st.download_button(label="Télécharger les résultats (CSV)", data=result_csv,
                                file_name="predictions_decrochage.csv", mime="text/csv")
                    except Exception as e:
                        st.error(f"Erreur lors de la prédiction batch : {str(e)}")
        except Exception as e:
            st.error(f"Erreur de lecture du fichier : {str(e)}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px 0; color: #9CA3AF;">
            <div style="font-size: 2.5rem; margin-bottom: 15px; color: #D1D5DB;">+</div>
            <p style="font-size: 0.9rem;">Glissez-déposez votre fichier CSV ici</p>
            <p style="font-size: 0.78rem;">ou cliquez pour parcourir — CSV, max 200 Mo</p>
        </div>
        """, unsafe_allow_html=True)
