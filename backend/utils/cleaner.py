import re

# Taille max raisonnable pour l'API (éviter timeouts / limites Groq)
MAX_TEXT_LENGTH = 15000


def clean_cv_text(raw: str) -> str:
    """
    Normalise le texte extrait OCR/PDF avant envoi à l'IA.
    """
    if not raw or not raw.strip():
        return ""

    text = raw.strip()

    # Normaliser espaces et sauts de ligne multiples
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Supprimer caractères de contrôle / bizarres
    text = "".join(c for c in text if c.isprintable() or c in "\n\t")

    # Tronquer si trop long (garder le début, souvent le plus informatif)
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH] + "\n[... texte tronqué ...]"

    return text.strip()
