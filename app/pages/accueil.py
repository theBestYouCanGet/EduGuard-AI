"""
Page d'accueil - Vue operationnelle
"""
import streamlit as st


def show(logo_path):
    st.markdown("""
    <h1 style="font-size: 1.8rem; font-weight: 700; color: #1B2A4A; margin-bottom: 8px;">
        Prediction du Decrochage Etudiant
    </h1>
    <p style="color: #6B7280; font-size: 0.95rem; line-height: 1.6;">
        Outil de detection du risque d'abandon scolaire. Saisissez les donnees d'un etudiant 
        ou importez un fichier CSV pour obtenir les predictions.
    </p>
    <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 25px 0 35px 0;">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-title">Prediction Individuelle</div>
            <div class="nav-card-desc">
                Analyser un etudiant via un formulaire structure. 
                Obtenez la prediction avec les probabilites et l'explication des facteurs determinants.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acceder", key="btn_pred", use_container_width=True):
            st.session_state.current_page = "pred_indiv"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-title">Prediction Batch</div>
            <div class="nav-card-desc">
                Analyser un groupe d'etudiants en important un fichier CSV. 
                Obtenez les resultats complets et exportez-les.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acceder", key="btn_batch", use_container_width=True):
            st.session_state.current_page = "pred_batch"
            st.rerun()

    # Section Adaptation FSBM
    st.markdown("""
    <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 30px 0 25px 0;">
    <h3 style="font-size: 1.1rem; font-weight: 600; color: #1B2A4A; margin-bottom: 15px;">
        Adaptation au Contexte Marocain
    </h3>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown("""
        <div class="nav-card" style="border-left: 4px solid #2563EB;">
            <div class="nav-card-title">Modele FSBM (Proof of Concept)</div>
            <div class="nav-card-desc">
                Modele entraine sur les donnees FSBM (6009 etudiants, 6 features). 
                Prediction binaire Abandon/Reinscription avec 84.6% de precision.
                Formulaire adapte aux filieres et mentions marocaines.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acceder au modele FSBM", key="btn_fsmb", use_container_width=True):
            st.session_state.current_page = "adapt_fsmb"
            st.rerun()

    with col4:
        st.markdown("""
        <div class="nav-card" style="border-left: 4px solid #D97706;">
            <div class="nav-card-title">Features Manquantes a Collecter</div>
            <div class="nav-card-desc">
                Le modele actuel utilise 6 features sur les 36 necessaires pour une prediction optimale. 
                30 features supplementaires sont a collecter aupres de l'administration FSBM.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-note">
        Modele Portugal (36 features, 3 classes) | Modele FSBM (6 features, 2 classes, POC)
    </div>
    """, unsafe_allow_html=True)
