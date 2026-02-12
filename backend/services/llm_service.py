import json
import re
import os
from typing import Dict, Any
from groq import Groq

# Initialiser le client Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def analyze_cv(text: str) -> Dict[str, Any]:
    """
    Analyse un texte de CV avec IA Groq pour extraire les informations structurées.
    
    Args:
        text (str): Le texte du CV
        
    Returns:
        dict: Informations structurées du CV au format JSON propre
    """
    if not text or not text.strip():
        return _get_empty_result("Aucun texte à analyser")
    
    try:
        # Nettoyer le texte
        cleaned_text = _clean_text(text)
        
        if len(cleaned_text) < 20:
            return _get_empty_result("Texte trop court pour l'analyse")
        
        # Appel direct à l'IA Groq sans validation préalable
        result = await _analyze_with_groq(cleaned_text)
        
        # Log pour debug
        print(f"Résultat brut de l'IA: {result}")
        
        cleaned_result = _validate_and_clean_result(result)
        
        # Log pour debug
        print(f"Résultat nettoyé: {cleaned_result}")
        
        # Validation post-analyse pour déterminer si c'est un CV
        if _is_empty_cv_result(cleaned_result):
            return _get_not_cv_result()
        
        return cleaned_result
        
    except Exception as e:
        print(f"Erreur analyse IA: {e}")
        return _get_fallback_result(text, str(e))

async def _analyze_with_groq(text: str) -> Dict[str, Any]:
    """
    Analyse avec Groq Llama 3.3 (modèle actuel)
    """
    prompt = f"""
    Tu es un expert en analyse de CV. Analyse ce texte et extrait les informations suivantes au format JSON strict et valide:

    {{
        "nom": "nom de famille trouvé ou 'Non trouvé'",
        "prenom": "prénom trouvé ou 'Non trouvé'", 
        "email": "adresse email trouvée ou 'Non trouvé'",
        "telephone": "numéro de téléphone trouvé ou 'Non trouvé'",
        "competences": ["compétence1", "compétence2", "compétence3"],
        "experiences": [
            {{"entreprise": "nom entreprise", "poste": "titre poste", "duree": "période"}},
            {{"entreprise": "nom entreprise", "poste": "titre poste", "duree": "période"}}
        ],
        "formations": [
            {{"ecole": "nom école", "diplome": "nom diplôme", "annee": "année"}},
            {{"ecole": "nom école", "diplome": "nom diplôme", "annee": "année"}}
        ]
    }}

    Règles importantes:
    - Si une information n'est pas trouvée, mets "Non trouvé" (pas null, pas undefined)
    - Pour les listes (competences, experiences, formations), si aucune donnée n'est trouvée, retourne des listes vides []
    - Pour les expériences et formations, si tu trouves des informations, crée des objets avec les clés demandées
    - Retourne UNIQUEMENT le JSON, sans aucun autre texte, sans ```json```
    - Le JSON doit être syntaxiquement valide
    - Sois précis et extrais toutes les informations pertinentes

    Texte du CV à analyser:
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Extraire le JSON proprement
        json_text = _extract_json_from_response(result_text)
        
        print(f"Texte brut de l'IA: {result_text}")
        print(f"JSON extrait: {json_text}")
        
        if json_text:
            return json.loads(json_text)
        else:
            raise Exception("Impossible d'extraire le JSON de la réponse")
            
    except Exception as e:
        print(f"Erreur Groq: {e}")
        raise e

def _extract_json_from_response(text: str) -> str:
    """
    Extrait le JSON de la réponse de l'IA
    """
    # Chercher le premier { et le dernier }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_text = text[start_idx:end_idx + 1]
        return json_text.strip()
    
    return ""

def _clean_text(text: str) -> str:
    """
    Nettoie le texte pour l'analyse
    """
    # Supprimer les caractères spéciaux excessifs
    text = re.sub(r'[^\w\s@.-]', ' ', text)
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def _validate_and_clean_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide et nettoie le résultat pour garantir un JSON propre
    """
    # Structure par défaut
    clean_result = {
        "nom": "Non trouvé",
        "prenom": "Non trouvé",
        "email": "Non trouvé", 
        "telephone": "Non trouvé",
        "competences": [],
        "experiences": [],
        "formations": []
    }
    
    # Valider et nettoyer chaque champ
    for key in clean_result.keys():
        if key in result:
            value = result[key]
            if key in ["competences", "experiences", "formations"]:
                # S'assurer que c'est une liste et convertir les chaînes en objets si nécessaire
                if isinstance(value, list):
                    clean_list = []
                    for item in value:
                        if isinstance(item, str):
                            # Essayer de parser la chaîne en dict
                            try:
                                import ast
                                parsed_item = ast.literal_eval(item)
                                if isinstance(parsed_item, dict):
                                    clean_list.append(parsed_item)
                                else:
                                    clean_list.append(item)
                            except:
                                clean_list.append(item)
                        elif isinstance(item, dict):
                            clean_list.append(item)
                        else:
                            clean_list.append(str(item) if item else "")
                    clean_result[key] = clean_list
                else:
                    clean_result[key] = []
            else:
                # S'assurer que c'est une chaîne
                clean_result[key] = str(value) if value else "Non trouvé"
    
    return clean_result

def _get_empty_result(reason: str) -> Dict[str, Any]:
    """
    Retourne un résultat vide avec une raison
    """
    return {
        "nom": "Non trouvé",
        "prenom": "Non trouvé",
        "email": "Non trouvé",
        "telephone": "Non trouvé", 
        "competences": [],
        "experiences": [],
        "formations": [],
        "error": reason
    }

def _is_empty_cv_result(result: Dict[str, Any]) -> bool:
    """
    Vérifie si le résultat de l'IA est vide (pas d'infos CV)
    """
    return (
        result.get("nom") == "Non trouvé" and
        result.get("prenom") == "Non trouvé" and
        result.get("email") == "Non trouvé" and
        result.get("telephone") == "Non trouvé" and
        len(result.get("competences", [])) == 0 and
        len(result.get("experiences", [])) == 0 and
        len(result.get("formations", [])) == 0
    )

def _is_likely_cv(text: str) -> bool:
    """
    Vérifie si le texte ressemble à un CV
    """
    # Mots-clés typiques des CV
    cv_keywords = [
        'expérience', 'expériences', 'experience', 'experiences',
        'formation', 'formations', 'diplôme', 'diplome', 'diplômes',
        'compétence', 'compétences', 'competence', 'competences',
        'parcours', 'professionnel', 'education', 'education',
        'emploi', 'poste', 'carrière', 'carriere',
        'curriculum', 'vitae', 'cv', 'resume'
    ]
    
    # Vérifier si le nom du fichier contient "cv"
    filename_indicators = ['cv', 'curriculum', 'vitae', 'resume']
    
    text_lower = text.lower()
    
    # Compter les mots-clés trouvés
    keyword_count = sum(1 for keyword in cv_keywords if keyword in text_lower)
    
    # Vérifier la structure (email, téléphone)
    has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
    
    # Score de confiance
    confidence_score = 0
    if keyword_count >= 2:
        confidence_score += 2
    if keyword_count >= 4:
        confidence_score += 2
    if has_email:
        confidence_score += 2
    if has_phone:
        confidence_score += 1
    if len(text) > 200:
        confidence_score += 1
    
    # Seuil minimum pour considérer que c'est un CV
    return confidence_score >= 3

def _get_not_cv_result() -> Dict[str, Any]:
    """
    Retourne un résultat indiquant que ce n'est pas un CV
    """
    return {
        "nom": "Non trouvé",
        "prenom": "Non trouvé",
        "email": "Non trouvé",
        "telephone": "Non trouvé",
        "competences": [],
        "experiences": [],
        "formations": [],
        "error": "Ce fichier ne semble pas être un CV. Veuillez télécharger un curriculum vitae valide."
    }

def _get_fallback_result(text: str, error: str) -> Dict[str, Any]:
    """
    Résultat de fallback avec extraction simple
    """
    # Extraction simple avec regex
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    
    return {
        "nom": "Non trouvé",
        "prenom": "Non trouvé",
        "email": email_match.group(0) if email_match else "Non trouvé",
        "telephone": phone_match.group(0) if phone_match else "Non trouvé",
        "competences": ["Extraction limitée"],
        "experiences": [],
        "formations": [],
        "error": f"Analyse IA échouée: {error}",
        "extraction_method": "fallback"
    }
