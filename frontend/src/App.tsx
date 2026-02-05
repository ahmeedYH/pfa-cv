import React, { useState } from "react";
import axios from "axios";

interface CVData {
  nom: string;
  prenom: string;
  email: string;
  telephone: string;
  competences: string[];
  experiences: Array<{ entreprise: string; poste: string; duree: string }>;
  formations: Array<{ ecole: string; diplome: string; annee: string }>;
  extraction_method?: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CVData | null>(null);
  const [error, setError] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError("");
      setResult(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        "http://localhost:8080/api/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erreur lors de l'analyse du CV");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        minHeight: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        padding: "20px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          backgroundColor: "white",
          borderRadius: "20px",
          boxShadow: "0 20px 40px rgba(0,0,0,0.1)",
          padding: "40px",
          maxWidth: "800px",
          width: "100%",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <h1
            style={{
              fontSize: "2.5rem",
              fontWeight: "700",
              color: "#2d3748",
              margin: "0",
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
            }}
          >
            PFA-CV
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              color: "#718096",
              marginTop: "10px",
              fontWeight: "400",
            }}
          >
            Transformez votre CV en données structurées prêtes pour
            l'intégration RH
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div
            style={{
              border: "3px dashed #cbd5e0",
              borderRadius: "15px",
              padding: "50px",
              textAlign: "center",
              marginBottom: "30px",
              transition: "all 0.3s ease",
              cursor: "pointer",
              backgroundColor: "#f7fafc",
            }}
          >
            <div
              style={{
                fontSize: "4rem",
                marginBottom: "20px",
              }}
            >
              📄
            </div>
            <label htmlFor="file-upload" style={{ cursor: "pointer" }}>
              <span
                style={{
                  color: "#667eea",
                  fontWeight: "600",
                  fontSize: "1.1rem",
                  marginRight: "10px",
                }}
              >
                Cliquez pour télécharger votre CV
              </span>
              <span style={{ color: "#a0aec0" }}>ou glissez-déposez</span>
              <input
                id="file-upload"
                type="file"
                style={{ display: "none" }}
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={handleFileChange}
              />
            </label>
            <p
              style={{
                fontSize: "0.9rem",
                color: "#a0aec0",
                marginTop: "15px",
              }}
            >
              PDF, PNG, JPG jusqu'à 10MB
            </p>
            {file && (
              <div
                style={{
                  marginTop: "20px",
                  padding: "10px 20px",
                  backgroundColor: "#edf2f7",
                  borderRadius: "10px",
                  color: "#4a5568",
                  fontSize: "0.95rem",
                  fontWeight: "500",
                }}
              >
                ✅ {file.name}
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={!file || loading}
            style={{
              width: "100%",
              backgroundColor:
                file && !loading
                  ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                  : "#e2e8f0",
              color: file && !loading ? "white" : "#a0aec0",
              padding: "18px",
              border: "none",
              borderRadius: "12px",
              fontSize: "1.1rem",
              fontWeight: "600",
              cursor: file && !loading ? "pointer" : "not-allowed",
              transition: "all 0.3s ease",
              boxShadow:
                file && !loading
                  ? "0 10px 25px rgba(102, 126, 234, 0.3)"
                  : "none",
            }}
          >
            {loading ? (
              <span>
                <span
                  style={{
                    display: "inline-block",
                    animation: "spin 1s linear infinite",
                  }}
                >
                  ⚙️
                </span>{" "}
                Analyse en cours...
              </span>
            ) : (
              "🚀 Analyser le CV"
            )}
          </button>
        </form>

        {error && (
          <div
            style={{
              marginTop: "25px",
              backgroundColor: "#fed7d7",
              border: "1px solid #fc8181",
              borderRadius: "10px",
              padding: "20px",
              color: "#c53030",
              fontWeight: "500",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginBottom: "5px",
              }}
            >
              <span style={{ marginRight: "10px", fontSize: "1.2rem" }}>
                ⚠️
              </span>
              <strong>Erreur:</strong>
            </div>
            {error}
          </div>
        )}

        {result && (
          <div style={{ marginTop: "40px" }}>
            <h2
              style={{
                color: "#2d3748",
                marginBottom: "25px",
                fontSize: "1.8rem",
                fontWeight: "700",
                textAlign: "center",
                paddingBottom: "15px",
                borderBottom: "3px solid #667eea",
              }}
            >
              📊 Résultats de l'analyse
            </h2>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
                gap: "25px",
              }}
            >
              <div
                style={{
                  background:
                    "linear-gradient(135deg, #f6f9fc 0%, #e9ecef 100%)",
                  padding: "25px",
                  borderRadius: "15px",
                  border: "1px solid #e2e8f0",
                }}
              >
                <h3
                  style={{
                    color: "#667eea",
                    marginBottom: "15px",
                    fontSize: "1.2rem",
                    fontWeight: "600",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <span style={{ marginRight: "10px", fontSize: "1.5rem" }}>
                    👤
                  </span>
                  Identité
                </h3>
                <p style={{ margin: "8px 0", color: "#4a5568" }}>
                  <strong>Nom:</strong> {result.prenom} {result.nom}
                </p>
                <p style={{ margin: "8px 0", color: "#4a5568" }}>
                  <strong>Email:</strong> {result.email}
                </p>
                <p style={{ margin: "8px 0", color: "#4a5568" }}>
                  <strong>Téléphone:</strong> {result.telephone}
                </p>
              </div>

              <div
                style={{
                  background:
                    "linear-gradient(135deg, #f6f9fc 0%, #e9ecef 100%)",
                  padding: "25px",
                  borderRadius: "15px",
                  border: "1px solid #e2e8f0",
                }}
              >
                <h3
                  style={{
                    color: "#667eea",
                    marginBottom: "15px",
                    fontSize: "1.2rem",
                    fontWeight: "600",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <span style={{ marginRight: "10px", fontSize: "1.5rem" }}>
                    🎯
                  </span>
                  Compétences
                </h3>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                  {result.competences && result.competences.length > 0 ? (
                    result.competences.map((skill, index) => (
                      <span
                        key={index}
                        style={{
                          background:
                            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                          color: "white",
                          padding: "6px 12px",
                          borderRadius: "20px",
                          fontSize: "0.85rem",
                          fontWeight: "500",
                          boxShadow: "0 2px 8px rgba(102, 126, 234, 0.3)",
                        }}
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <div
                      style={{
                        padding: "15px",
                        backgroundColor: "#f7fafc",
                        borderRadius: "8px",
                        color: "#718096",
                        textAlign: "center",
                        width: "100%",
                      }}
                    >
                      Aucune compétence trouvée
                    </div>
                  )}
                </div>
              </div>

              <div
                style={{
                  background:
                    "linear-gradient(135deg, #f6f9fc 0%, #e9ecef 100%)",
                  padding: "25px",
                  borderRadius: "15px",
                  border: "1px solid #e2e8f0",
                }}
              >
                <h3
                  style={{
                    color: "#667eea",
                    marginBottom: "15px",
                    fontSize: "1.2rem",
                    fontWeight: "600",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <span style={{ marginRight: "10px", fontSize: "1.5rem" }}>
                    💼
                  </span>
                  Expériences
                </h3>
                {result.experiences && result.experiences.length > 0 ? (
                  result.experiences.map((exp, index) => (
                    <div
                      key={index}
                      style={{
                        marginBottom: "15px",
                        padding: "10px",
                        backgroundColor: "white",
                        borderRadius: "8px",
                      }}
                    >
                      <p
                        style={{
                          margin: "5px 0",
                          fontWeight: "600",
                          color: "#2d3748",
                        }}
                      >
                        {exp.poste}
                      </p>
                      <p
                        style={{
                          margin: "3px 0",
                          color: "#718096",
                          fontSize: "0.9rem",
                        }}
                      >
                        {exp.entreprise}
                      </p>
                      <p
                        style={{
                          margin: "3px 0",
                          color: "#a0aec0",
                          fontSize: "0.85rem",
                        }}
                      >
                        {exp.duree}
                      </p>
                    </div>
                  ))
                ) : (
                  <div
                    style={{
                      padding: "15px",
                      backgroundColor: "#f7fafc",
                      borderRadius: "8px",
                      color: "#718096",
                      textAlign: "center",
                    }}
                  >
                    Aucune expérience trouvée
                  </div>
                )}
              </div>

              <div
                style={{
                  background:
                    "linear-gradient(135deg, #f6f9fc 0%, #e9ecef 100%)",
                  padding: "25px",
                  borderRadius: "15px",
                  border: "1px solid #e2e8f0",
                }}
              >
                <h3
                  style={{
                    color: "#667eea",
                    marginBottom: "15px",
                    fontSize: "1.2rem",
                    fontWeight: "600",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <span style={{ marginRight: "10px", fontSize: "1.5rem" }}>
                    🎓
                  </span>
                  Formations
                </h3>
                {result.formations && result.formations.length > 0 ? (
                  result.formations.map((formation, index) => (
                    <div
                      key={index}
                      style={{
                        marginBottom: "15px",
                        padding: "10px",
                        backgroundColor: "white",
                        borderRadius: "8px",
                      }}
                    >
                      <p
                        style={{
                          margin: "5px 0",
                          fontWeight: "600",
                          color: "#2d3748",
                        }}
                      >
                        {formation.diplome}
                      </p>
                      <p
                        style={{
                          margin: "3px 0",
                          color: "#718096",
                          fontSize: "0.9rem",
                        }}
                      >
                        {formation.ecole}
                      </p>
                      <p
                        style={{
                          margin: "3px 0",
                          color: "#a0aec0",
                          fontSize: "0.85rem",
                        }}
                      >
                        {formation.annee}
                      </p>
                    </div>
                  ))
                ) : (
                  <div
                    style={{
                      padding: "15px",
                      backgroundColor: "#f7fafc",
                      borderRadius: "8px",
                      color: "#718096",
                      textAlign: "center",
                    }}
                  >
                    Aucune formation trouvée
                  </div>
                )}
              </div>
            </div>

            {result.extraction_method && (
              <div
                style={{
                  marginTop: "30px",
                  textAlign: "center",
                  fontSize: "0.9rem",
                  color: "#718096",
                  padding: "15px",
                  backgroundColor: "#f7fafc",
                  borderRadius: "10px",
                }}
              >
                🤖 Méthode d'extraction: {result.extraction_method}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
