import React, { useState, useRef } from "react";
import "./App.css";

// Debug: Log environment variable
console.log("API URL:", process.env.REACT_APP_API_URL);
console.log("Environment:", process.env.NODE_ENV);

interface UploadedFile {
  name: string;
  size: number;
  type: string;
}

interface ExtractedData {
  nom: string;
  prenom: string;
  email: string;
  telephone: string;
  experiences: Array<{
    entreprise: string;
    poste: string;
    duree: string;
  }>;
  formations: Array<{
    ecole: string;
    diplome: string;
    annee: string;
  }>;
  competences: string[];
  error?: string;
}

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [extractedData, setExtractedData] = useState<ExtractedData | null>(
    null,
  );
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    const validTypes = [
      "application/pdf",
      "image/png",
      "image/jpeg",
      "image/jpg",
    ];
    const maxSize = 10 * 1024 * 1024;

    if (!validTypes.includes(file.type)) {
      alert("Type de fichier non supporté. Utilisez PDF, PNG ou JPG.");
      return;
    }

    if (file.size > maxSize) {
      alert("Fichier trop volumineux. Maximum 10MB.");
      return;
    }

    setUploadedFile({
      name: file.name,
      size: file.size,
      type: file.type,
    });
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    setUploadedFile(null);
    setIsAnalyzing(false);
    setExtractedData(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleAnalyze = async () => {
    if (uploadedFile) {
      setIsAnalyzing(true);

      try {
        // Get the actual file from the file input
        const fileInput = fileInputRef.current;
        if (!fileInput || !fileInput.files || !fileInput.files[0]) {
          throw new Error("Aucun fichier sélectionné");
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(
          `${process.env.REACT_APP_API_URL || "http://localhost:8001"}/api/analyze`,
          {
            method: "POST",
            body: formData,
          },
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(
            errorData.detail || `Erreur HTTP: ${response.status}`,
          );
        }

        const data = await response.json();
        setExtractedData(data);
        setIsAnalyzing(false);
      } catch (error) {
        console.error("Error:", error);
        setIsAnalyzing(false);
        alert(
          `Erreur lors de l'analyse: ${error instanceof Error ? error.message : "Erreur inconnue"}`,
        );
      }
    }
  };

  const handleNewAnalysis = () => {
    setExtractedData(null);
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className={`app ${isDarkMode ? "dark-mode" : ""}`}>
      <header className="app-header">
        <div className="logo">
          <div className="logo-icon">
            <svg
              viewBox="0 0 40 40"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M20 8L20 32M20 8L12 16M20 8L28 16M20 32C15.5817 32 12 28.4183 12 24C12 19.5817 15.5817 16 20 16C24.4183 16 28 19.5817 28 24C28 28.4183 24.4183 32 20 32Z"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <span className="logo-text">TalentFlow</span>
        </div>

        <div className="theme-toggle">
          <span className="theme-label">Mode Sombre</span>
          <button
            className="toggle-button"
            onClick={() => setIsDarkMode(!isDarkMode)}
            aria-label="Toggle dark mode"
          >
            <div
              className={`toggle-slider ${isDarkMode ? "active" : ""}`}
            ></div>
          </button>
        </div>
      </header>

      <div className="main-container">
        <main className="main-card">
          <div className="card-content">
            <h1 className="main-title">TalentFlow</h1>
            <p className="subtitle">
              Transformez votre CV en données
              <br />
              structurées prêtes pour l'intégration RH
            </p>

            <div
              className={`upload-area ${dragActive ? "drag-active" : ""}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="upload-icon">
                <svg
                  viewBox="0 0 80 80"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M40 20V50M40 20L30 30M40 20L50 30"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M25 40C25 40 20 40 20 45C20 50 25 50 25 50C25 50 20 50 20 45C20 40 25 40 25 40"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <circle
                    cx="40"
                    cy="45"
                    r="20"
                    stroke="currentColor"
                    strokeWidth="3"
                  />
                  <path
                    className="wave wave-1"
                    d="M25 48C28 46 32 46 35 48C38 50 42 50 45 48"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                  <path
                    className="wave wave-2"
                    d="M35 52C38 50 42 50 45 52C48 54 52 54 55 52"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                </svg>
              </div>

              <p className="upload-text">
                Cliquez pour téléverser votre CV
                <br />
                ou glisez-déposez
              </p>

              <div className="file-types">
                <span className="file-badge pdf">PDF</span>
                <span className="file-badge doc">DOC</span>
                <span className="file-type-text">
                  PDF, PNG, JPG jusqu'à 10MB
                </span>
                <span className="file-badge jpg">JPG</span>
                <span className="file-badge png">PNG</span>
                {uploadedFile && (
                  <span
                    className="file-badge delete"
                    onClick={handleDelete}
                    title="Supprimer le fichier"
                  >
                    ✕
                  </span>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                className="file-input"
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={handleChange}
              />
            </div>

            {uploadedFile && !isAnalyzing && (
              <div className="uploaded-file-info">
                <span className="check-icon">✓</span>
                <span>{uploadedFile.name}</span>
                <span className="file-size">
                  ({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)
                </span>
              </div>
            )}

            {isAnalyzing && (
              <div className="analyzing-container">
                <div className="spinner"></div>
                <p className="analyzing-text">Analyse en cours...</p>
                <p className="analyzing-subtext">
                  Extraction des données du CV
                </p>
              </div>
            )}

            {extractedData && !isAnalyzing && (
              <div className="results-container">
                {extractedData.error ? (
                  <div className="data-card">
                    <h3 className="card-title">❌ Erreur</h3>
                    <div className="card-content">
                      <p className="error-message">{extractedData.error}</p>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="results-header">
                      <h2 className="results-title">✓ Données extraites</h2>
                      <button
                        className="copy-json-btn"
                        onClick={() => {
                          navigator.clipboard.writeText(
                            JSON.stringify(extractedData, null, 2),
                          );
                        }}
                      >
                        📋 Copier JSON
                      </button>
                    </div>

                    <div className="data-cards">
                      {/* Personal Info Card */}
                      <div className="data-card">
                        <h3 className="card-title">
                          👤 Informations personnelles
                        </h3>
                        <div className="card-content">
                          <div className="info-row">
                            <span className="info-label">Nom complet:</span>
                            <span className="info-value">
                              {extractedData.prenom} {extractedData.nom}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="info-label">Email:</span>
                            <span className="info-value">
                              {extractedData.email}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="info-label">Téléphone:</span>
                            <span className="info-value">
                              {extractedData.telephone}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Experience Card */}
                      <div className="data-card">
                        <h3 className="card-title">
                          💼 Expérience professionnelle
                        </h3>
                        <div className="card-content">
                          {extractedData.experiences &&
                          extractedData.experiences.length > 0 ? (
                            extractedData.experiences.map(
                              (exp: any, index: number) => (
                                <div key={index} className="experience-item">
                                  <div className="exp-header">
                                    <span className="exp-poste">
                                      {exp.poste}
                                    </span>
                                    <span className="exp-periode">
                                      {exp.duree}
                                    </span>
                                  </div>
                                  <div className="exp-entreprise">
                                    {exp.entreprise}
                                  </div>
                                </div>
                              ),
                            )
                          ) : (
                            <p className="no-data">Aucune expérience trouvée</p>
                          )}
                        </div>
                      </div>

                      {/* Education Card */}
                      <div className="data-card">
                        <h3 className="card-title">🎓 Formation</h3>
                        <div className="card-content">
                          {extractedData.formations &&
                          extractedData.formations.length > 0 ? (
                            extractedData.formations.map(
                              (form: any, index: number) => (
                                <div key={index} className="formation-item">
                                  <div className="form-header">
                                    <span className="form-diplome">
                                      {form.diplome}
                                    </span>
                                    <span className="form-annee">
                                      {form.annee}
                                    </span>
                                  </div>
                                  <div className="form-etablissement">
                                    {form.ecole}
                                  </div>
                                </div>
                              ),
                            )
                          ) : (
                            <p className="no-data">Aucune formation trouvée</p>
                          )}
                        </div>
                      </div>

                      {/* Skills Card */}
                      <div className="data-card">
                        <h3 className="card-title">⚡ Compétences</h3>
                        <div className="card-content">
                          <div className="skills-grid">
                            {extractedData.competences &&
                            extractedDataData.competences.length > 0 ? (
                              extractedDataData.competences.map(
                                (skill: any, index: number) => (
                                  <span key={index} className="skill-badge">
                                    {skill}
                                  </span>
                                ),
                              )
                            ) : (
                              <p className="no-data">
                                Aucune compétence trouvée
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="results-actions">
                      <button
                        className="download-json-btn"
                        onClick={() => {
                          const blob = new Blob(
                            [JSON.stringify(extractedData, null, 2)],
                            { type: "application/json" },
                          );
                          const url = URL.createObjectURL(blob);
                          const a = document.createElement("a");
                          a.href = url;
                          a.download = `cv_${uploadedFile?.name.replace(/\.[^/.]+$/, "")}_data.json`;
                          a.click();
                        }}
                      >
                        ⬇️ Télécharger JSON
                      </button>
                      <button
                        className="new-analysis-btn"
                        onClick={handleNewAnalysis}
                      >
                        🔄 Nouvelle analyse
                      </button>
                    </div>
                  </>
                )}
              </div>
            )}

            <button
              className="analyze-button"
              onClick={uploadedFile ? handleAnalyze : onButtonClick}
              disabled={isAnalyzing}
              style={{ display: extractedData ? "none" : "block" }}
            >
              {isAnalyzing
                ? "Analyse en cours..."
                : uploadedFile
                  ? "Analyser le CV"
                  : "Téléverser un fichier"}
            </button>

            <div
              className="progress-indicator"
              style={{ display: extractedData ? "none" : "flex" }}
            >
              <div className="progress-dot active"></div>
              <div className="progress-dot"></div>
              <div className="progress-dot"></div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
