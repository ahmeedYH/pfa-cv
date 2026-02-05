import io
from backend.services.pdf_service import extract_text_from_file
from backend.services.ocr_service import extract_text_from_image
from backend.services.llm_service import analyze_cv


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
        # Extraire texte depuis PDF ou image
        text = extract_text_from_file(file)
        if not text.strip():
            raise ValueError("Le fichier ne contient aucun texte exploitable")
        return await analyze_cv(text)

    except Exception as e:
        return {"error": f"Erreur lors de l'extraction du texte: {str(e)}"}


async def process_image_cv(image_file) -> dict:
    """
    Analyse une image directement
    """
    try:
        text = extract_text_from_image(image_file.file.read())
        if not text.strip():
            raise ValueError("L'image ne contient aucun texte exploitable")
        return await analyze_cv(text)

    except Exception as e:
        return {"error": f"Erreur lors de l'extraction du texte: {str(e)}"}
