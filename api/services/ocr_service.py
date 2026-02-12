import subprocess
from PIL import Image
import io
import os
import tempfile

def extract_text_from_image(image_data):
    """
    Extrait le texte d'une image en utilisant Tesseract OCR
    Retourne le texte extrait ou lève une exception en cas d'erreur
    """
    try:
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_path = temp_file.name
            
            # Sauvegarder l'image
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            image.save(temp_path)
            
            # Utiliser tesseract directement
            result = subprocess.run(
                ['tesseract', temp_path, 'stdout', '-l', 'fra'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Nettoyer
            os.unlink(temp_path)
            
            text = result.stdout.strip()
            return text if text else ""
            
    except subprocess.CalledProcessError as e:
        # Nettoyer en cas d'erreur
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        raise Exception(f"Erreur Tesseract: {e.stderr}")
    except Exception as e:
        # Nettoyer en cas d'erreur
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        raise Exception(f"Erreur OCR: {str(e)}")
