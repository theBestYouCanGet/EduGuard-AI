"""
Shared utilities for the Streamlit app
Model loading, prediction, SHAP, feature definitions, CSV utilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Font setup
try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# ========== PATHS ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ========== FEATURE DEFINITIONS ==========
FEATURE_GROUPS = {
    "Informations Personnelles": {
        "Marital Status": {"type": "select", "label": "État civil", "options": {
            1: "Célibataire", 2: "Marié(e)", 3: "Veuf/Veuve", 
            4: "Séparé(e)", 5: "Concubin(e)", 6: "Divorcé(e)"
        }},
        "Gender": {"type": "select", "label": "Genre", "options": {1: "Homme", 0: "Femme"}},
        "Age at enrollment": {"type": "slider", "label": "Âge à l'inscription", "min": 17, "max": 70, "default": 20},
        "Nacionality": {"type": "select", "label": "Nationalité", "options": {
            1: "Portugais(e)", 2: "Allemand(e)", 6: "Espagnol(e)", 11: "Italien(e)",
            13: "Néerlandais(e)", 14: "Anglais(e)", 17: "Lituanien(e)", 21: "Angolais(e)",
            22: "Cap-verdien(e)", 24: "Guinéen(e)", 25: "Mozambicain(e)", 26: "Santoméen(e)",
            32: "Turc/Turque", 41: "Brésilien(e)", 62: "Roumain(e)", 100: "Moldave",
            101: "Mexicain(e)", 103: "Ukrainien(e)", 105: "Russe", 108: "Cubain(e)",
            109: "Colombien(e)"
        }},
        "Displaced": {"type": "select", "label": "Déplacé(e)", "options": {0: "Non", 1: "Oui"}},
        "International": {"type": "select", "label": "Étudiant international", "options": {0: "Non", 1: "Oui"}},
    },
    "Informations Académiques": {
        "Application mode": {"type": "select", "label": "Mode de candidature", "options": {
            1: "1ère phase - contingent général", 2: "Ordre des 6 institutions", 
            5: "1ère phase - contingent spécial (Açores)", 7: "Titulaires d'autres cours supérieurs",
            10: "Ordre des 3 institutions", 15: "Étudiant international (bachelier)",
            16: "1ère phase - contingent spécial (Madère)", 17: "2ème phase - contingent général",
            18: "3ème phase - contingent général", 26: "Ordre des 3 institutions",
            27: "2ème phase - contingent spécial", 39: "Plus de 23 ans",
            42: "Transfert", 43: "Changement de cours", 44: "Diplôme spécialisé",
            51: "1ère phase - contingent spécial", 53: "1ère phase - contingent spécial",
            57: "Changement d'institution/course"
        }},
        "Application order": {"type": "slider", "label": "Ordre de candidature", "min": 0, "max": 9, "default": 1},
        "Course": {"type": "select", "label": "Filière", "options": {
            33: "Technologies de production de bio-carburants", 171: "Animation et conception culturelle",
            8014: "Service social (soir)", 9003: "Agronomie", 9070: "Communication design",
            9085: "Infirmier vétérinaire", 9119: "Ingénierie informatique",
            9130: "Informatique", 9147: "Gestion d'entreprise", 9238: "Services sociaux",
            9254: "Tourisme", 9500: "Soins infirmiers", 9556: "Hygiène bucco-dentaire",
            9670: "Gestion de la communication", 9773: "Journalisme et communication",
            9853: "Éducation de base", 9991: "Gestion (soir)"
        }},
        "Daytime/evening attendance": {"type": "select", "label": "Horaire", "options": {1: "Jour", 0: "Soir"}},
        "Previous qualification": {"type": "select", "label": "Qualification antérieure", "options": {
            1: "Secondaire", 2: "Baccalauréat", 3: "Licence", 4: "Master",
            5: "Doctorat", 6: "Cours supérieur", 9: "12ème année - non achevé",
            10: "11ème année - non achevé", 12: "Autre - 11ème année",
            14: "15ème année", 15: "14ème année", 19: "13ème année",
            38: "Basique 3ème cycle", 39: "Licence (1er cycle)", 40: "Master (2ème cycle)",
            42: "Doctorat (3ème cycle)", 43: "Master - spécialisation"
        }},
        "Previous qualification (grade)": {"type": "slider", "label": "Note qualification antérieure", "min": 95.0, "max": 190.0, "default": 132.0, "step": 0.5},
        "Admission grade": {"type": "slider", "label": "Note d'admission", "min": 95.0, "max": 190.0, "default": 127.0, "step": 0.5},
        "Educational special needs": {"type": "select", "label": "Besoins éducatifs spéciaux", "options": {0: "Non", 1: "Oui"}},
    },
    "Situation Familiale": {
        "Mother's qualification": {"type": "select", "label": "Qualification de la mère", "options": {
            1: "Secondaire", 2: "Baccalauréat", 3: "Licence", 4: "Master", 5: "Doctorat",
            6: "Cours supérieur", 9: "12ème année - non achevé", 10: "11ème année - non achevé",
            11: "7ème année (ancien)", 12: "Autre - 11ème année", 14: "15ème année",
            18: "Cours commerce", 19: "13ème année", 22: "Technicien",
            26: "7ème année", 27: "2ème cycle du secondaire", 29: "9ème année - non achevé",
            30: "8ème année", 34: "Inconnu", 35: "Ne sait ni lire ni écrire",
            36: "Sait lire sans avoir fréquenté", 37: "4ème année (en cours)",
            38: "Basique 3ème cycle", 39: "Licence (1er cycle)", 40: "Master (2ème cycle)",
            41: "Spécialisation supérieur", 42: "Doctorat (3ème cycle)", 43: "Master - spécialisation",
            44: "Technicien supérieur"
        }},
        "Father's qualification": {"type": "select", "label": "Qualification du père", "options": {
            1: "Secondaire", 2: "Baccalauréat", 3: "Licence", 4: "Master", 5: "Doctorat",
            6: "Cours supérieur", 9: "12ème année - non achevé", 10: "11ème année - non achevé",
            11: "7ème année (ancien)", 12: "Autre - 11ème année", 13: "2ème cycle complémentaire",
            14: "15ème année", 18: "Cours commerce", 19: "13ème année", 20: "Cours artistique",
            22: "Technicien", 25: "2ème cycle complémentaire", 26: "7ème année",
            27: "2ème cycle du secondaire", 29: "9ème année - non achevé", 30: "8ème année",
            31: "Cours administration", 33: "Cours technique", 34: "Inconnu",
            35: "Ne sait ni lire ni écrire", 36: "Sait lire sans avoir fréquenté",
            37: "4ème année (en cours)", 38: "Basique 3ème cycle", 39: "Licence (1er cycle)",
            40: "Master (2ème cycle)", 41: "Spécialisation supérieur", 42: "Doctorat (3ème cycle)",
            43: "Master - spécialisation", 44: "Technicien supérieur"
        }},
        "Mother's occupation": {"type": "select", "label": "Profession de la mère", "options": {
            0: "Étudiant(e)", 1: "Représentants du pouvoir législatif", 2: "Intellectuels et scientifiques",
            3: "Techniciens niveau intermédiaire", 4: "Employés de bureau", 5: "Personnel de service",
            6: "Agriculteurs", 7: "Artisans", 8: "Opérateurs machines", 9: "Travailleurs non qualifiés",
            10: "Forces armées", 90: "Autre situation", 99: "Non applicable",
            122: "Professionnels de la santé", 123: "Professeurs", 125: "Spécialistes TIC",
            131: "Scientifiques", 132: "Professionnels libéraux", 134: "Cadres intermédiaires",
            141: "Employés de bureau", 143: "Employés de service", 144: "Vendeurs",
            151: "Travailleurs agricoles", 152: "Travailleurs construction", 153: "Travailleurs industrie",
            171: "Travailleurs non qualifiés", 173: "Travailleurs manuels",
            175: "Ouvriers construction", 191: "Nettoyeurs", 192: "Manutentionnaires",
            193: "Vendeurs de rue", 194: "Collecteurs de déchets"
        }},
        "Father's occupation": {"type": "select", "label": "Profession du père", "options": {
            0: "Étudiant(e)", 1: "Représentants du pouvoir législatif", 2: "Intellectuels et scientifiques",
            3: "Techniciens niveau intermédiaire", 4: "Employés de bureau", 5: "Personnel de service",
            6: "Agriculteurs", 7: "Artisans", 8: "Opérateurs machines", 9: "Travailleurs non qualifiés",
            10: "Forces armées", 90: "Autre situation", 99: "Non applicable",
            101: "Officiers forces armées", 102: "Sergents forces armées", 103: "Autres forces armées",
            112: "Directeurs services", 114: "Directeurs hôtellerie", 121: "Scientifiques",
            122: "Professionnels de la santé", 123: "Professeurs", 124: "Professionnels finance",
            131: "Scientifiques", 132: "Professionnels libéraux", 134: "Cadres intermédiaires",
            135: "Techniciens informatique", 141: "Employés de bureau", 143: "Employés de service",
            144: "Vendeurs", 151: "Travailleurs agricoles", 152: "Travailleurs construction",
            153: "Travailleurs industrie", 154: "Travailleurs graphiques", 161: "Opérateurs extraction",
            163: "Opérateurs construction", 171: "Travailleurs non qualifiés", 172: "Nettoyeurs",
            174: "Aides soignants", 175: "Ouvriers construction", 181: "Conducteurs",
            182: "Chauffeurs", 183: "Manutentionnaires", 192: "Manutentionnaires",
            193: "Vendeurs de rue", 194: "Collecteurs de déchets", 195: "Vendeurs rue"
        }},
    },
    "Situation Financière": {
        "Debtor": {"type": "select", "label": "Débiteur", "options": {0: "Non", 1: "Oui"}},
        "Tuition fees up to date": {"type": "select", "label": "Frais à jour", "options": {0: "Non", 1: "Oui"}},
        "Scholarship holder": {"type": "select", "label": "Boursier", "options": {0: "Non", 1: "Oui"}},
    },
    "Unités Curriculaires — Semestre 1": {
        "Curricular units 1st sem (credited)": {"type": "slider", "label": "UC validées (S1)", "min": 0, "max": 20, "default": 0},
        "Curricular units 1st sem (enrolled)": {"type": "slider", "label": "UC inscrites (S1)", "min": 0, "max": 26, "default": 6},
        "Curricular units 1st sem (evaluations)": {"type": "slider", "label": "UC évaluées (S1)", "min": 0, "max": 45, "default": 8},
        "Curricular units 1st sem (approved)": {"type": "slider", "label": "UC approuvées (S1)", "min": 0, "max": 26, "default": 5},
        "Curricular units 1st sem (grade)": {"type": "slider", "label": "Moyenne UC (S1)", "min": 0.0, "max": 19.0, "default": 10.5, "step": 0.5},
        "Curricular units 1st sem (without evaluations)": {"type": "slider", "label": "UC sans évaluation (S1)", "min": 0, "max": 12, "default": 0},
    },
    "Unités Curriculaires — Semestre 2": {
        "Curricular units 2nd sem (credited)": {"type": "slider", "label": "UC validées (S2)", "min": 0, "max": 19, "default": 0},
        "Curricular units 2nd sem (enrolled)": {"type": "slider", "label": "UC inscrites (S2)", "min": 0, "max": 23, "default": 6},
        "Curricular units 2nd sem (evaluations)": {"type": "slider", "label": "UC évaluées (S2)", "min": 0, "max": 33, "default": 8},
        "Curricular units 2nd sem (approved)": {"type": "slider", "label": "UC approuvées (S2)", "min": 0, "max": 20, "default": 4},
        "Curricular units 2nd sem (grade)": {"type": "slider", "label": "Moyenne UC (S2)", "min": 0.0, "max": 19.0, "default": 10.0, "step": 0.5},
        "Curricular units 2nd sem (without evaluations)": {"type": "slider", "label": "UC sans évaluation (S2)", "min": 0, "max": 12, "default": 0},
    },
    "Indicateurs Macroéconomiques": {
        "Unemployment rate": {"type": "slider", "label": "Taux de chômage (%)", "min": 7.6, "max": 16.2, "default": 11.6, "step": 0.1},
        "Inflation rate": {"type": "slider", "label": "Taux d'inflation (%)", "min": -0.8, "max": 3.7, "default": 1.2, "step": 0.1},
        "GDP": {"type": "slider", "label": "PIB (%)", "min": -4.1, "max": 3.5, "default": 0.0, "step": 0.01},
    },
}

ALL_FEATURES = [
    'Marital Status', 'Application mode', 'Application order', 'Course',
    'Daytime/evening attendance', 'Previous qualification',
    'Previous qualification (grade)', 'Nacionality', "Mother's qualification",
    "Father's qualification", "Mother's occupation", "Father's occupation",
    'Admission grade', 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder',
    'Age at enrollment', 'International',
    'Curricular units 1st sem (credited)',
    'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)',
    'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',
    'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)',
    'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)',
    'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)',
    'Curricular units 2nd sem (without evaluations)', 'Unemployment rate',
    'Inflation rate', 'GDP'
]

CLASS_NAMES = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
CLASS_LABELS_FR = {0: "Abandon", 1: "Inscrit", 2: "Diplômé"}
CLASS_COLORS = {0: "#DC2626", 1: "#D97706", 2: "#16A34A"}

# ========== MODEL LOADING (with version compatibility) ==========
@st.cache_resource
def load_model():
    """Load XGBoost model - native JSON format first, then pickle fallback"""
    from xgboost import XGBClassifier
    import pickle
    
    json_path = os.path.join(MODELS_DIR, "model.json")
    pkl_path = os.path.join(MODELS_DIR, "model.pkl")
    
    # Try native format first (works across numpy/xgboost versions)
    if os.path.exists(json_path):
        try:
            model = XGBClassifier()
            model.load_model(json_path)
            return model
        except Exception:
            pass
    
    # Fallback to pickle
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement du modèle : {e}")
        st.info("Essayez : pip install numpy==1.26.4 scikit-learn==1.6.1 xgboost==2.1.3")
        st.stop()

@st.cache_resource
def load_scaler():
    """Load scaler - joblib first, then pickle fallback"""
    import pickle
    
    joblib_path = os.path.join(MODELS_DIR, "scaler.joblib")
    pkl_path = os.path.join(MODELS_DIR, "scaler.pkl")
    
    if os.path.exists(joblib_path):
        try:
            import joblib
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return joblib.load(joblib_path)
        except Exception:
            pass
    
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement du scaler : {e}")
        st.stop()

@st.cache_resource
def load_encoder():
    """Load encoder - joblib first, then pickle fallback"""
    import pickle
    
    joblib_path = os.path.join(MODELS_DIR, "encoder.joblib")
    pkl_path = os.path.join(MODELS_DIR, "encoder.pkl")
    
    if os.path.exists(joblib_path):
        try:
            import joblib
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return joblib.load(joblib_path)
        except Exception:
            pass
    
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(pkl_path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement de l'encodeur : {e}")
        st.stop()

@st.cache_resource
def load_shap_explainer():
    """Load SHAP explainer - try v2 first, then original"""
    import pickle
    
    v2_path = os.path.join(MODELS_DIR, "shap_explainer_v2.pkl")
    orig_path = os.path.join(MODELS_DIR, "shap_explainer.pkl")
    
    path = v2_path if os.path.exists(v2_path) else orig_path
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.warning(f"Impossible de charger l'explicateur SHAP : {e}")
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
    result_df["Prédiction"] = [CLASS_LABELS_FR[int(p)] for p in predictions]
    result_df["Prob_Abandon"] = [float(p[0]) for p in probas]
    result_df["Prob_Inscrit"] = [float(p[1]) for p in probas]
    result_df["Prob_Diplômé"] = [float(p[2]) for p in probas]
    return result_df

# ========== SHAP ==========
def _get_shap_values(input_dict):
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
    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        class_shap = shap_values[0, :, class_idx]
        expected_val = explainer.expected_value[class_idx]
    elif isinstance(shap_values, list):
        class_shap = shap_values[class_idx][0]
        expected_val = explainer.expected_value[class_idx]
    else:
        class_shap = shap_values[0]
        expected_val = explainer.expected_value
    return class_idx, class_shap, expected_val, X_scaled

def generate_shap_bar(input_dict):
    result = _get_shap_values(input_dict)
    if result is None:
        return None
    class_idx, class_shap, expected_val, _ = result
    class_shap_flat = np.array([float(v) for v in class_shap])
    feature_importance = list(zip(ALL_FEATURES, class_shap_flat))
    feature_importance.sort(key=lambda x: abs(float(x[1])), reverse=True)
    top_features = feature_importance[:15]
    top_features.reverse()
    names = [f[0] for f in top_features]
    values = [float(f[1]) for f in top_features]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    colors = ['#DC2626' if v < 0 else '#16A34A' for v in values]
    ax.barh(range(len(names)), values, color=colors, height=0.6, edgecolor='none')
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9, color='#374151')
    ax.tick_params(axis='x', colors='#9CA3AF')
    ax.set_xlabel('Impact SHAP', color='#6B7280', fontsize=11)
    class_label = CLASS_LABELS_FR[class_idx]
    ax.set_title(f'Explication SHAP — {class_label}', color='#1B2A4A', fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='x', alpha=0.15, color='#9CA3AF')
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color('#E5E7EB')
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#16A34A', label='Augmente la probabilité'),
        Patch(facecolor='#DC2626', label='Diminue la probabilité')
    ]
    ax.legend(handles=legend_elements, loc='lower right',
              facecolor='#F9FAFB', edgecolor='#E5E7EB',
              labelcolor='#374151', fontsize=9)
    plt.tight_layout()
    return fig

# ========== CSV ==========
def get_csv_template():
    return pd.DataFrame(columns=ALL_FEATURES)

def validate_csv(df):
    issues = []
    missing_cols = [col for col in ALL_FEATURES if col not in df.columns]
    if missing_cols:
        issues.append(f"Colonnes manquantes: {', '.join(missing_cols[:5])}")
    for col in ALL_FEATURES:
        if col not in df.columns:
            df[col] = 0
    for col in ALL_FEATURES:
        if col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            except:
                pass
    if issues:
        return False, "; ".join(issues), df[ALL_FEATURES]
    return True, "Fichier valide", df[ALL_FEATURES]
