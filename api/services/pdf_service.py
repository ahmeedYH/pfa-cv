import io
import tempfile
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from services.ocr_service import extract_text_from_image

def extract_text_from_file(file):
    """
    Extrait le texte d'un fichier (PDF ou image)
    Retourne le texte extrait ou lève une exception en cas d'erreur
    """
    try:
        content = file.file.read()
        
        if not content:
            raise Exception("Fichier vide")
            
        filename = file.filename.lower() if file.filename else ""
        
        if filename.endswith(".pdf"):
            return _extract_from_pdf(content)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            return extract_text_from_image(content)
        else:
            raise Exception(f"Type de fichier non supporté: {filename}")
            
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction du texte: {str(e)}")

def _extract_from_pdf(content):
    """
    Extrait le texte d'un PDF avec fallback OCR
    """
    try:
        # Essayer l'extraction directe du texte d'abord
        reader = PdfReader(io.BytesIO(content))
        text_parts = []
        
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text.strip())
            except Exception as e:
                print(f"Erreur extraction page {page_num}: {e}")
                continue
        
        if text_parts:
            full_text = "\n".join(text_parts)
            if len(full_text.strip()) > 50:  # Si on a assez de texte
                return full_text.strip()
        
        # Fallback: OCR sur les images du PDF
        return _pdf_ocr_fallback(content)
        
    except Exception as e:
        print(f"Erreur extraction PDF directe: {e}")
        # Fallback: OCR
        return _pdf_ocr_fallback(content)

def _pdf_ocr_fallback(content):
    """
    Fallback OCR pour les PDF
    """
    try:
        images = convert_from_bytes(content)
        text_parts = []
        
        for i, image in enumerate(images):
            try:
                page_text = extract_text_from_image(image)
                if page_text and page_text.strip():
                    text_parts.append(page_text.strip())
            except Exception as e:
                print(f"Erreur OCR page {i}: {e}")
                continue
        
        if text_parts:
            return "\n".join(text_parts)
        else:
            raise Exception("Aucun texte trouvé dans le PDF même avec OCR")
            
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du PDF: {str(e)}")
