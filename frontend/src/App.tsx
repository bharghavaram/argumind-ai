import React, { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

interface ModelAnalysis {
  model: string;
  raw_response: string;
  tokens_used: number;
  error?: string;
}

interface AnalysisResult {
  topic: string;
  argument: string;
  model_analyses: Record<string, ModelAnalysis>;
  verdict: {
    synthesis: string;
    models_used: string[];
  };
}

const MODELS = [
  { id: "gpt4", name: "GPT-4o", color: "#10a37f" },
  { id: "claude", name: "Claude 3.5", color: "#d4a853" },
  { id: "mistral", name: "Mistral Large", color: "#ff7000" },
];

export default function App() {
  const [topic, setTopic] = useState("");
  const [argument, setArgument] = useState("");
  const [selectedModels, setSelectedModels] = useState(["gpt4", "claude", "mistral"]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const toggleModel = (id: string) => {
    setSelectedModels((prev) =>
      prev.includes(id) ? prev.filter((m) => m !== id) : [...prev, id]
    );
  };

  const analyse = async () => {
    if (!topic.trim() || !argument.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/arguments/analyse`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, argument, models: selectedModels }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setResult(await res.json());
    } catch (e: any) {
      setError(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "system-ui", maxWidth: 900, margin: "0 auto", padding: 32 }}>
      <h1 style={{ color: "#1a1a2e" }}>🧠 Argumind AI</h1>
      <p style={{ color: "#555" }}>Multi-LLM Argument Analysis & Verdict System</p>

      <div style={{ background: "#f8f9fa", borderRadius: 12, padding: 24, marginBottom: 24 }}>
        <label style={{ fontWeight: 600 }}>Topic</label>
        <input
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g. Remote work increases productivity"
          style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ddd", marginTop: 6, marginBottom: 16, fontSize: 15, boxSizing: "border-box" }}
        />
        <label style={{ fontWeight: 600 }}>Argument to Analyse</label>
        <textarea
          value={argument}
          onChange={(e) => setArgument(e.target.value)}
          placeholder="e.g. Stanford research shows 13% productivity boost in remote workers..."
          rows={4}
          style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ddd", marginTop: 6, marginBottom: 16, fontSize: 15, boxSizing: "border-box" }}
        />
        <div style={{ marginBottom: 16 }}>
          <label style={{ fontWeight: 600 }}>Models</label>
          <div style={{ display: "flex", gap: 10, marginTop: 8 }}>
            {MODELS.map((m) => (
              <button
                key={m.id}
                onClick={() => toggleModel(m.id)}
                style={{
                  padding: "8px 16px",
                  borderRadius: 20,
                  border: "2px solid",
                  borderColor: m.color,
                  background: selectedModels.includes(m.id) ? m.color : "white",
                  color: selectedModels.includes(m.id) ? "white" : m.color,
                  cursor: "pointer",
                  fontWeight: 600,
                  fontSize: 14,
                }}
              >
                {m.name}
              </button>
            ))}
          </div>
        </div>
        <button
          onClick={analyse}
          disabled={loading || !topic.trim() || !argument.trim() || selectedModels.length === 0}
          style={{
            padding: "12px 32px",
            background: "#1a1a2e",
            color: "white",
            border: "none",
            borderRadius: 8,
            fontSize: 16,
            fontWeight: 600,
            cursor: "pointer",
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading ? "Analysing..." : "🔍 Analyse Argument"}
        </button>
      </div>

      {error && (
        <div style={{ background: "#fff0f0", border: "1px solid #ffcccc", borderRadius: 8, padding: 16, color: "#c00", marginBottom: 16 }}>
          {error}
        </div>
      )}

      {result && (
        <div>
          <h2>Model Analyses</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 16, marginBottom: 24 }}>
            {Object.entries(result.model_analyses).map(([key, analysis]) => {
              const m = MODELS.find((x) => x.id === key);
              return (
                <div key={key} style={{ background: "#fff", border: `2px solid ${m?.color || "#ddd"}`, borderRadius: 12, padding: 16 }}>
                  <h3 style={{ color: m?.color, margin: "0 0 8px" }}>{m?.name || key}</h3>
                  {analysis.error ? (
                    <p style={{ color: "#c00" }}>Error: {analysis.error}</p>
                  ) : (
                    <>
                      <p style={{ fontSize: 13, color: "#555", lineHeight: 1.6 }}>{analysis.raw_response?.slice(0, 400)}...</p>
                      <p style={{ fontSize: 12, color: "#888", marginTop: 8 }}>Tokens: {analysis.tokens_used}</p>
                    </>
                  )}
                </div>
              );
            })}
          </div>

          <div style={{ background: "#1a1a2e", color: "white", borderRadius: 12, padding: 24 }}>
            <h2 style={{ margin: "0 0 12px", color: "#ffd700" }}>⚖️ Synthesised Verdict</h2>
            <p style={{ lineHeight: 1.7, color: "#e0e0e0" }}>{result.verdict.synthesis}</p>
            <p style={{ fontSize: 13, color: "#aaa", marginTop: 12 }}>
              Models used: {result.verdict.models_used.join(", ")}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
