from fastapi import APIRouter, File, UploadFile, HTTPException

from backend.services.pdf_service import extract_text_from_file
from backend.services.llm_service import analyze_cv
from backend.utils.cleaner import clean_cv_text

router = APIRouter(prefix="/api", tags=["cv"])

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.get("/health")
def health():
    return {"status": "ok", "service": "pfa-cv"}


@router.post("/analyze")
async def analyze_cv_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "Aucun fichier fourni")

    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400,
            f"Type de fichier non accepté. Autorisés: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "Fichier trop volumineux (max 10 Mo)")

    # Reconstruct a minimal file-like for extract_text_from_file (it uses .file.read() and .filename)
    class FileLike:
        def __init__(self, data: bytes, filename: str):
            self._data = data
            self.filename = filename

        @property
        def file(self):
            import io
            return io.BytesIO(self._data)

    file_like = FileLike(content, file.filename)
    try:
        raw_text = extract_text_from_file(file_like)
    except Exception as e:
        raise HTTPException(500, f"Erreur lors de l'extraction du texte: {str(e)}")

    if not raw_text or not raw_text.strip():
        raise HTTPException(400, "Aucun texte extrait du document. Vérifiez que le fichier est lisible (PDF avec texte ou image claire).")

    cleaned_text = clean_cv_text(raw_text)
    result = await analyze_cv(cleaned_text)

    if "error" in result:
        raise HTTPException(502, result["error"])

    return result
