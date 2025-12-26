import os
import json
from groq import Groq
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

def analyze_cv_with_ai(text_cv):
    """
    Envoie le texte brut du CV à l'IA (Groq/Llama3)
    et retourne un objet Python (Dictionnaire/JSON).
    """

    # 1. Vérification de sécurité
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "Clé API manquante dans le fichier .env"}

    # 2. Initialisation du client Groq
    client = Groq(api_key=api_key)

    # 3. LE PROMPT (C'est ici que tu donnes les ordres à l'IA)
    # On lui demande de répondre UNIQUEMENT en JSON.
    system_prompt = """
    Tu es un expert en recrutement et en extraction de données.
    Ton rôle est d'analyser un texte de CV et d'extraire les informations suivantes au format JSON strict.
    
    Champs requis :
    - nom (string)
    - prenom (string)
    - email (string ou null)
    - telephone (string ou null)
    - competences (liste de strings, ex: ["Python", "Java"])
    - experiences (liste d'objets avec "poste", "entreprise", "annee")
    - formation (liste d'objets avec "diplome", "ecole", "annee")
    - langue (string, langue principale du CV detectée, ex: "fr" ou "en")

    Règles importantes :
    1. Renvoie SEULEMENT le JSON. Pas de phrase d'intro ("Voici le JSON...").
    2. Si une info est introuvable, mets null.
    3. Corrige les fautes d'orthographe évidentes dans les compétences.
    """

    try:
        # 4. Envoi de la requête à l'IA
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Voici le texte du CV à analyser : \n\n{text_cv}"}
            ],
            model="llama3-70b-8192", # Modèle très puissant et gratuit sur Groq
            temperature=0, # 0 = On veut des faits précis, pas de créativité
            response_format={"type": "json_object"} # Force le mode JSON
        )

        # 5. Récupération et nettoyage de la réponse
        result_content = chat_completion.choices[0].message.content

        # On transforme le texte reçu en véritable objet Python
        data = json.loads(result_content)
        return data

    except json.JSONDecodeError:
        return {"error": "L'IA a mal formaté le JSON.", "raw": result_content}
    except Exception as e:
        return {"error": f"Erreur API : {str(e)}"}