from backend.services.llm_service import analyze_cv_with_ai

# Simulation d'un texte sale extrait d'un PDF par ton binôme
fake_cv_text = """
CURRICULUM VITAE
Dupont Jean
Ingénieur Logiciel
Email: jean.dupont@email.com | Tel: 06 12 34 56 78

EXPERIENCES
2022-2024 : Développeur Fullstack chez TechCorp. Utilisation de Python et React.
2020-2022 : Stagiaire Java chez OldSchool Company.

COMPETENCES
Pyton, Javva, Docker, SQL, Anglais courant.

FORMATION
Master Informatique - Université de Paris (2020)
"""

print("--- Envoi à l'IA en cours... ---")
resultat = analyze_cv_with_ai(fake_cv_text)

print("\n--- RÉSULTAT JSON ---")
import json
print(json.dumps(resultat, indent=4, ensure_ascii=False))