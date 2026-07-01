"""
Page de connexion
Fix: block-container devient la carte — header HTML + inputs natifs sont dans le meme conteneur visuel

Sécurité : les mots de passe sont lus depuis les variables d'environnement (.env)
config.yaml ne contient que le NOM de la variable (password_env), jamais la valeur.
"""
import streamlit as st
import os
import base64

# Charger les variables d'environnement depuis .env
try:
    from dotenv import load_dotenv
    # Chercher .env à la racine du projet (parent du dossier app/)
    _env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(_env_path):
        load_dotenv(_env_path)
except ImportError:
    # python-dotenv n'est pas installé — on continue avec les variables d'environnement existantes
    pass


def _img_to_data_url(path: str) -> str:
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


def show(config, logo_path):
    logo_url = _img_to_data_url(logo_path)

    st.markdown(f"""
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    header[data-testid="stHeader"] {{ display: none !important; }}

    .stApp {{ background: #F0F2F6 !important; }}

    .block-container {{
        padding-top: 6vh !important;
        padding-bottom: 0 !important;
    }}

    /* LA CARTE : on cible le stVerticalBlock de la colonne centrale */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) > div[data-testid="stVerticalBlock"] {{
        background: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(27,42,74,0.13), 0 2px 8px rgba(27,42,74,0.05);
        overflow: hidden;
    }}

    /* Padding du body de la carte (tout sauf le header HTML qui gère son propre padding) */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) > div[data-testid="stVerticalBlock"]
    > div.element-container:not(:first-child) {{
        padding-left: 32px;
        padding-right: 32px;
    }}

    /* Labels */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stTextInput > label {{
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        color: #1B2A4A !important;
    }}

    /* Inputs */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stTextInput input {{
        border-radius: 8px !important;
        border: 1.5px solid #D1D5DB !important;
        background: #FAFAFA !important;
        font-size: 0.92rem !important;
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stTextInput input:focus {{
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
        background: #FFFFFF !important;
    }}

    /* Bouton Se connecter */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {{
        width: 100% !important;
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {{
        background: #1D4ED8 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    logo_tag = f'<img src="{logo_url}" style="width:68px;height:68px;object-fit:contain;background:#fff;border-radius:12px;padding:6px;margin:0 auto 14px auto;display:block;" alt="FSBM"/>' if logo_url else ""

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        # Header navy — DANS la colonne, sera dans le même stVerticalBlock
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1B2A4A 0%,#243B6B 100%);
                    padding:30px 32px 26px 32px; text-align:center; color:#fff;">
            {logo_tag}
            <div style="font-size:1.15rem;font-weight:700;margin-bottom:5px;line-height:1.3;">
                Prédiction du Décrochage Étudiant
            </div>
            <div style="font-size:0.78rem;color:#B4C0D9;">
                FSBM — Université Hassan II Casablanca
            </div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Identifiant", placeholder="Entrez votre identifiant", key="login_username")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe", key="login_password")
        login_clicked = st.button("Se connecter", key="btn_login", use_container_width=True)

        st.markdown("""
        <div style="text-align:center;font-size:0.73rem;color:#9CA3AF;
                    padding:14px 32px 22px 32px;border-top:1px solid #F3F4F6;margin-top:10px;">
            Accès réservé aux chefs de filière
        </div>
        """, unsafe_allow_html=True)

    if login_clicked:
        if not username or not password:
            st.error("Veuillez saisir votre identifiant et votre mot de passe.")
            return
        users = config.get("users", {})
        user = users.get(username)
        # Sécurité : récupérer le mot de passe depuis les variables d'environnement
        # config.yaml contient password_env = "EDUGUARD_DEFAULT_PASSWORD" (le NOM de la variable)
        # On lit la VALEUR depuis os.environ
        if user:
            password_env_var = user.get("password_env", "EDUGUARD_DEFAULT_PASSWORD")
            expected_password = os.environ.get(password_env_var, "")
            # Rétrocompatibilité : si l'ancien champ "password" existe toujours dans config.yaml
            if not expected_password and "password" in user:
                expected_password = user["password"]
            if expected_password and password == expected_password:
                st.session_state.logged_in    = True
                st.session_state.user_name    = user["name"]
                st.session_state.user_dept    = user["department"]
                st.session_state.current_page = "accueil"
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
        else:
            st.error("Identifiant ou mot de passe incorrect.")
