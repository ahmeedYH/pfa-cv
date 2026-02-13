import io
from services.pdf_service import extract_text_from_file
from services.ocr_service import extract_text_from_image
from services.llm_service import analyze_cv


async def process_text_cv(text: str) -> dict:
    """
    Analyse un texte brut directement avec LLM
    """
    return await analyze_cv(text)


async def process_file_cv(file) -> dict:
    """
    Analyse un fichier : PDF ou image
    """
    try:
        # Vérifier si le nom du fichier contient "cv"
        filename = file.filename.lower() if hasattr(file, 'filename') else ''
        
        # Extraire texte depuis PDF ou image
        text = extract_text_from_file(file)
        if not text.strip():
            raise ValueError("Le fichier ne contient aucun texte exploitable")
        
        # Analyser le texte pour déterminer si c'est un CV
        result = await analyze_cv(text)
        
        # Si le résultat contient une erreur "pas un CV", la retourner
        if "error" in result and "pas être un CV" in result["error"]:
            return result
            
        # Si le nom du fichier ne contient pas "cv" mais l'analyse détecte un CV, accepter
        if 'cv' not in filename and 'curriculum' not in filename and 'vitae' not in filename:
            # Vérifier si l'analyse a trouvé des infos de CV
            has_cv_content = (
                result.get("nom") != "Non trouvé" or 
                result.get("prenom") != "Non trouvé" or
                result.get("email") != "Non trouvé" or
                len(result.get("competences", [])) > 0 or
                len(result.get("experiences", [])) > 0 or
                len(result.get("formations", [])) > 0
            )
            
            if has_cv_content:
                # C'est probablement un CV mal nommé, accepter
                return result
            else:
                # Ce n'est vraiment pas un CV
                return {
                    "nom": "Non trouvé",
                    "prenom": "Non trouvé",
                    "email": "Non trouvé",
                    "telephone": "Non trouvé",
                    "competences": [],
                    "experiences": [],
                    "formations": [],
                    "error": "Ce fichier ne semble pas contenir d'informations de CV valides. Veuillez télécharger un curriculum vitae avec des informations claires (nom, email, expériences, formations, ou compétences)."
                }
        
        return result

    except Exception as e:
        return {"error": f"Erreur lors de l'extraction du texte: {str(e)}"}


async def process_image_cv(image_file) -> dict:
    """
    Analyse une image directement
    """
    try:
        # Vérifier si le nom du fichier contient "cv"
        filename = image_file.filename.lower() if hasattr(image_file, 'filename') else ''
        
        # Extraire texte de l'image
        text = extract_text_from_image(image_file.file.read())
        if not text.strip():
            raise ValueError("L'image ne contient aucun texte exploitable")
        
        # Analyser le texte pour déterminer si c'est un CV
        result = await analyze_cv(text)
        
        # Si le résultat contient une erreur "pas un CV", la retourner
        if "error" in result and "pas être un CV" in result["error"]:
            return result
            
        # Si le nom du fichier ne contient pas "cv" mais l'analyse détecte un CV, accepter
        if 'cv' not in filename and 'curriculum' not in filename and 'vitae' not in filename:
            # Vérifier si l'analyse a trouvé des infos de CV
            has_cv_content = (
                result.get("nom") != "Non trouvé" or 
                result.get("prenom") != "Non trouvé" or
                result.get("email") != "Non trouvé" or
                len(result.get("competences", [])) > 0 or
                len(result.get("experiences", [])) > 0 or
                len(result.get("formations", [])) > 0
            )
            
            if has_cv_content:
                # C'est probablement un CV mal nommé, accepter
                return result
            else:
                # Ce n'est vraiment pas un CV
                return {
                    "nom": "Non trouvé",
                    "prenom": "Non trouvé",
                    "email": "Non trouvé",
                    "telephone": "Non trouvé",
                    "competences": [],
                    "experiences": [],
                    "formations": [],
                    "error": "Cette image ne semble pas contenir d'informations de CV valides. Veuillez télécharger un curriculum vitae avec des informations claires (nom, email, expériences, formations, ou compétences)."
                }
        
        return result

    except Exception as e:
        return {"error": f"Erreur lors de l'extraction du texte: {str(e)}"}
