from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from services.cv_service import process_text_cv, process_file_cv, process_image_cv

router = APIRouter(prefix="/api/cv", tags=["CV"])

# -------------------------
# Analyse texte brut
# -------------------------
@router.post("/analyze/text")
async def analyze_text(text: str = Form(...)):
    """
    Recevoir du texte brut et retourner JSON LLM
    """
    result = await process_text_cv(text)
    return JSONResponse(content=result)


# -------------------------
# Analyse fichier (PDF ou image)
# -------------------------
@router.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    """
    Recevoir un fichier (PDF ou image) et retourner JSON LLM
    """
    result = await process_file_cv(file)
    return JSONResponse(content=result)


# -------------------------
# Analyse image directement
# -------------------------
@router.post("/analyze/image")
async def analyze_image(image: UploadFile = File(...)):
    """
    Recevoir une image et retourner JSON LLM
    """
    result = await process_image_cv(image)
    return JSONResponse(content=result)
