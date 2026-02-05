# pfa-cv — Roadmap (2 jours)

Objectif : avoir une app utilisable (upload CV → extraction texte → analyse IA → affichage JSON) en 2 jours.

---

## Jour 1 — Backend + API

### 1. Corriger le bug PDF (15 min)
- **Fichier:** `backend/services/pdf_service.py`
- **Problème:** Après `file.file.read()`, le flux est consommé ; `PdfReader(file.file)` lit un flux vide.
- **Fix:** Lire une seule fois en bytes, puis utiliser `io.BytesIO(content)` pour `PdfReader` et `content` pour `convert_from_bytes`.

### 2. Créer l’app FastAPI (30 min)
- **Fichier:** `backend/main.py`
- Créer l’instance FastAPI.
- Monter le routeur API (ex: `/api`).
- Activer CORS pour le frontend (origins du front en dev).
- Point d’entrée : `uvicorn backend.main:app --reload`.

### 3. Créer les endpoints API (1 h)
- **Fichier:** `backend/api.py`
- **POST `/api/analyze`** (ou `/api/upload`)
  - Reçoit un fichier (PDF/image) via `File()`.
  - Appelle `pdf_service.extract_text_from_file(file)`.
  - (Optionnel) Passe le texte par `cleaner` si tu l’implémentes.
  - Appelle `llm_service.analyze_cv_with_ai(text)`.
  - Retourne le JSON structuré (ou 400/500 en cas d’erreur).
- **GET `/api/health`** (optionnel) pour vérifier que l’API répond.

### 4. Tester l’API à la main (30 min)
- Lancer le backend.
- Tester avec Postman, curl ou Thunder Client : envoi d’un PDF → vérifier la réponse JSON.
- Corriger les imports si besoin (ex: `from backend.services...` vs `from services...` selon d’où tu lances).

### 5. (Optionnel) Nettoyage du texte (30 min)
- **Fichier:** `backend/utils/cleaner.py`
- Fonction qui reçoit le texte brut OCR/PDF et : normalise espaces/sauts de ligne, supprime caractères bizarres, coupe si trop long pour l’API.
- L’appeler dans l’endpoint avant `analyze_cv_with_ai`.

**Fin Jour 1 :** API fonctionnelle, testée avec un vrai PDF.

---

## Jour 2 — Frontend + finition

### 6. Page d’upload simple (1 h)
- **Fichier:** `Frontend/index.html`
- Formulaire : input `type="file"` (accept: `.pdf, .png, .jpg, .jpeg`).
- Bouton « Analyser » qui envoie le fichier en POST vers `http://localhost:8000/api/analyze` (ou l’URL de ton backend).
- Afficher un message « En cours... » pendant la requête.

### 7. Affichage du résultat (1 h)
- Après réponse réussie : afficher le JSON formaté (nom, prénom, email, compétences, expériences, formation).
- Soit en `<pre>` pour du JSON brut, soit en petites sections HTML (titres + listes).
- En cas d’erreur : afficher le message d’erreur retourné par l’API.

### 8. Amélioration UX rapide (30 min)
- Style minimal (CSS dans la page ou fichier séparé) pour que ce soit lisible.
- Désactiver le bouton pendant l’envoi pour éviter les double-clics.
- (Optionnel) Drag & drop de fichier.

### 9. README et lancement (30 min)
- **Fichier:** `README.md`
- Sections : description du projet, prérequis (Python, Tesseract, clé Groq), installation (`pip install -r requirements.txt`), configuration (`.env` avec `GROQ_API_KEY`), lancer le backend, ouvrir le frontend.
- Vérifier que tout fonctionne en suivant le README from scratch (dans un autre dossier ou après `git clone`).

### 10. Buffer / polish (reste du temps)
- Gestion d’erreurs côté front (réseau, fichier trop gros, type non supporté).
- Limiter la taille du fichier côté API (ex: 10 Mo) avec FastAPI.
- Corriger les derniers bugs ou incohérences d’affichage.

---

## Résumé

| Jour | Objectif principal |
|------|--------------------|
| **Jour 1** | Bug PDF corrigé, `main.py` + `api.py` avec POST analyze, API testée |
| **Jour 2** | Frontend upload + affichage résultat, README, tests de bout en bout |

À la fin des 2 jours, tu dois pouvoir : ouvrir la page → choisir un CV (PDF/image) → cliquer Analyser → voir les infos extraites par l’IA.
