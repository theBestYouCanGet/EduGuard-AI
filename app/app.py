"""
Prediction du Decrochage Etudiant - FSBM
Application Streamlit pour les chefs de filiere
"""

import streamlit as st
import yaml
import os
import base64

st.set_page_config(
    page_title="Prediction Decrochage - FSBM",
    page_icon=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_fsbm.png") if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_fsbm.png")) else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CONFIG ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo_fsbm.png")
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

PAGE_KEYS = ["accueil", "pred_indiv", "pred_batch", "adapt_fsmb"]
PAGE_DISPLAY = {
    "accueil": "Accueil",
    "pred_indiv": "Prediction Individuelle",
    "pred_batch": "Prediction Batch",
    "adapt_fsmb": "Adaptation FSBM"
}

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _img_to_data_url(path: str) -> str:
    """Convertit une image locale en data URL.
    Evite la dependance a PIL / st.image() qui peut casser selon l'environnement.
    """
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "gif": "image/gif", "webp": "image/webp", "svg": "image/svg+xml"}.get(ext, "image/png")
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        return f"data:{mime};base64,{data}"
    except Exception:
        return ""


# ========== SESSION STATE ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_dept" not in st.session_state:
    st.session_state.user_dept = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "accueil"


# ========== CSS GLOBAL ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body { font-family: 'Inter', sans-serif; }
    p, h1, h2, h3, h4, h5, h6, label, input, textarea, select, button {
        font-family: 'Inter', sans-serif;
    }

    /* FIX expanders Streamlit 1.44+ : empêche arrow_right de s'afficher en texte */
    [data-testid="stExpander"] details > summary > span > svg,
    [data-testid="stExpander"] details > summary svg { display: inline-block !important; }
    [data-testid="stExpander"] details > summary > span[data-testid="stExpanderToggleIcon"] {
        font-family: inherit;
    }
    /* Cacher le texte brut si le SVG ne se charge pas */
    [data-testid="stExpander"] details > summary > span.st-emotion-cache-* { display: none; }
    .stApp { background-color: #FFFFFF; }

    /* ================================================================
       FIX Streamlit 1.45+ : icone arrow_right des expanders
       La classe font-icon utilise une police speciale — ne pas overrider
       ================================================================ */
    [data-testid="stExpander"] summary svg,
    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"],
    [data-testid="stExpander"] summary span[aria-hidden="true"],
    .streamlit-expanderHeader svg { display: block !important; }

    /* Cacher le texte brut de l'icone si jamais il s'affiche encore */
    [data-testid="stExpander"] summary > div > p:first-child:only-child,
    [data-testid="stExpander"] details > summary > span.label { display: none; }

    /* Style propre des expanders */
    [data-testid="stExpander"] details > summary {
        background: #F8FAFC !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        color: #1B2A4A !important;
    }
    [data-testid="stExpander"] details[open] > summary {
        border-radius: 10px 10px 0 0 !important;
    }
    [data-testid="stExpander"] details > summary:hover {
        background: #F0F4FF !important;
    }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* =====================================================================
       SIDEBAR - Style nav moderne, fiable, base sur des BOUTONS
       On evite les hack CSS fragiles sur stRadio - on cible stButton a la place
       ===================================================================== */
    [data-testid="stSidebar"] {
        background: #1B2A4A !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: #1B2A4A !important;
    }
    /* Masquer la nav par defaut de Streamlit (multipage) - pas utilisee ici */
    [data-testid="stSidebarNav"] { display: none !important; }

    /* Forcer la sidebar a toujours etre visible apres connexion */
    [data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 280px !important;
    }

    /* ====== Texte sous le logo ====== */
    .sidebar-user-name {
        font-weight: 600;
        font-size: 0.92rem;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .sidebar-user-dept {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    .sidebar-section-label {
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #64748B;
        margin: 14px 0 8px 4px;
    }

    /* ====== Boutons de navigation dans la sidebar ======
       On cible TOUS les boutons de la sidebar - ils servent tous a la navigation */
    [data-testid="stSidebar"] .stButton {
        margin-bottom: 4px;
        width: 100%;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #CBD5E1 !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        width: 100% !important;
        text-align: left !important;
        padding: 10px 14px !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.07) !important;
        color: #FFFFFF !important;
        border-color: rgba(255,255,255,0.1) !important;
    }
    [data-testid="stSidebar"] .stButton > button p {
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }

    /* Le bouton Deconnexion - il est en bas, juste apres un <hr>.
       On lui donne un style distinct (bordure + hover rouge). */
    [data-testid="stSidebar"] hr + .stButton > button,
    [data-testid="stSidebar"] hr + div > .stButton > button {
        margin-top: 18px !important;
        background: transparent !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }
    [data-testid="stSidebar"] hr + .stButton > button:hover,
    [data-testid="stSidebar"] hr + div > .stButton > button:hover {
        background: rgba(248, 113, 113, 0.1) !important;
        color: #FCA5A5 !important;
        border-color: #F87171 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
        margin: 14px 0 !important;
    }

    /* =====================================================================
       BOUTONS DU CONTENU PRINCIPAL
       ===================================================================== */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 10px 24px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    .stDownloadButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .stDownloadButton > button:hover {
        background-color: #1D4ED8 !important;
    }

    [data-testid="stFileUploader"] {
        border: 2px dashed #D1D5DB;
        border-radius: 12px;
        padding: 20px;
        background-color: #F9FAFB;
    }
    .stSuccess { border-left: 4px solid #16A34A !important; }
    .stWarning { border-left: 4px solid #D97706 !important; }
    .stError   { border-left: 4px solid #DC2626 !important; }

    /* ====== CARDS ====== */
    .nav-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 40px 30px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .nav-card:hover {
        border-color: #2563EB;
        box-shadow: 0 4px 20px rgba(37,99,235,0.08);
    }
    .nav-card-title { font-size: 1.2rem; font-weight: 600; color: #1B2A4A; margin-bottom: 10px; }
    .nav-card-desc  { font-size: 0.88rem; color: #6B7280; margin-bottom: 25px; line-height: 1.6; }

    /* ====== RESULT CARD ====== */
    .result-card { border-radius: 12px; padding: 30px; text-align: center; margin-bottom: 20px; }
    .result-card.dropout  { background: #FEF2F2; border: 2px solid #DC2626; }
    .result-card.enrolled { background: #FFFBEB; border: 2px solid #D97706; }
    .result-card.graduate { background: #F0FDF4; border: 2px solid #16A34A; }
    .result-card.reinscrit { background: #F0FDF4; border: 2px solid #16A34A; }
    .result-label { font-size: 0.9rem; color: #6B7280; margin-bottom: 4px; }
    .result-value { font-size: 2rem; font-weight: 700; margin: 6px 0; }
    .result-value.dropout  { color: #DC2626; }
    .result-value.enrolled { color: #D97706; }
    .result-value.graduate { color: #16A34A; }
    .result-value.reinscrit { color: #16A34A; }
    .result-alert  { font-size: 0.85rem; color: #6B7280; margin-top: 6px; }

    /* ====== PROB BARS ====== */
    .prob-row { margin: 10px 0; }
    .prob-header { display: flex; justify-content: space-between; margin-bottom: 5px; }
    .prob-label  { font-size: 0.85rem; color: #374151; }
    .prob-value  { font-size: 0.85rem; font-weight: 600; }
    .prob-bar-bg { background: #F3F4F6; border-radius: 6px; height: 20px; overflow: hidden; }
    .prob-bar { height: 100%; border-radius: 6px; }
    .prob-bar.red    { background: #DC2626; }
    .prob-bar.orange { background: #D97706; }
    .prob-bar.green  { background: #16A34A; }

    /* ====== RISK ====== */
    .risk-box { border-radius: 10px; padding: 14px; text-align: center; margin: 18px 0; }
    .risk-box.critique { background: #FEF2F2; border: 1px solid #DC2626; }
    .risk-box.eleve    { background: #FFF7ED; border: 1px solid #D97706; }
    .risk-box.moyen    { background: #FFFBEB; border: 1px solid #EAB308; }
    .risk-box.faible   { background: #F0FDF4; border: 1px solid #16A34A; }
    .risk-level { font-size: 1.1rem; font-weight: 700; }
    .risk-level.critique { color: #DC2626; }
    .risk-level.eleve    { color: #D97706; }
    .risk-level.moyen    { color: #EAB308; }
    .risk-level.faible   { color: #16A34A; }
    .risk-detail { font-size: 0.8rem; color: #6B7280; margin-left: 10px; }

    /* ====== SUMMARY ====== */
    .summary-card {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }
    .summary-number { font-size: 1.8rem; font-weight: 700; }
    .summary-number.red    { color: #DC2626; }
    .summary-number.orange { color: #D97706; }
    .summary-number.green  { color: #16A34A; }
    .summary-number.blue   { color: #2563EB; }
    .summary-label { font-size: 0.8rem; color: #6B7280; margin-top: 4px; }
    .alert-box {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 18px;
        font-size: 0.85rem;
        color: #DC2626;
        font-weight: 500;
    }
    .footer-note {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.78rem;
        font-style: italic;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #F3F4F6;
    }
</style>
""", unsafe_allow_html=True)


# ========== PAGE DE CONNEXION ==========
if not st.session_state.logged_in:
    from pages.login import show as show_login
    show_login(load_config(), LOGO_PATH)
    st.stop()


# ========== SIDEBAR (apres connexion) ==========
with st.sidebar:
    # Logo (via data URL - evite la dependance a PIL/st.image)
    logo_url = _img_to_data_url(LOGO_PATH)
    if logo_url:
        st.markdown(
            f'<div style="text-align:center; margin-bottom: 6px;">'
            f'<img src="{logo_url}" alt="FSBM" style="width:160px; max-width:100%; '
            f'background:#FFFFFF; border-radius:8px; padding:6px; box-sizing:border-box;"/>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Texte sous le logo
    st.markdown("""
    <div style="text-align: center; padding: 2px 0 10px 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
        <div style="font-size: 0.58rem; color: #94A3B8; line-height: 1.4;">
            Faculte des Sciences Ben M'Sick<br>Universite Hassan II Casablanca
        </div>
    </div>
    """, unsafe_allow_html=True)

    # User info
    st.markdown(f"""
    <div style="padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 4px;">
        <div class="sidebar-user-name">{st.session_state.user_name}</div>
        <div class="sidebar-user-dept">{st.session_state.user_dept}</div>
    </div>
    """, unsafe_allow_html=True)

    # Label de section
    st.markdown('<div class="sidebar-section-label">Navigation</div>',
                unsafe_allow_html=True)

    # ----- Boutons de navigation -----
    # Bouton simple = navigation ultra fiable.  Le bouton actif est prefixe
    # d'un triangle pour indiquer visuellement la page courante.
    current = st.session_state.get("current_page", "accueil")

    for key in PAGE_KEYS:
        label = PAGE_DISPLAY[key]
        is_active = (key == current)
        # Indicateur visuel d'activite : un triangle a droite du label
        if is_active:
            btn_label = f"\u25C0  {label}"   # ◀ en prefixe
        else:
            btn_label = f"\u2003\u2003{label}"  # indentation pour aligner
        if st.button(btn_label, key=f"nav_{key}", use_container_width=True):
            st.session_state.current_page = key
            st.rerun()

    st.markdown("---")

    # Bouton Deconnexion
    if st.button("Deconnexion", key="btn_logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_dept = ""
        st.session_state.current_page = "accueil"
        st.rerun()


# ========== PAGES (apres connexion) ==========
current_page = st.session_state.get("current_page", "accueil")
if current_page == "accueil":
    from pages.accueil import show as show_accueil
    show_accueil(LOGO_PATH)
elif current_page == "pred_indiv":
    from pages.prediction import show as show_prediction
    show_prediction()
elif current_page == "pred_batch":
    from pages.batch import show as show_batch
    show_batch()
elif current_page == "adapt_fsmb":
    from pages.prediction_fsmb import show as show_fsmb
    show_fsmb()
