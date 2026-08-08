/**
 * VigilIA App — Componente raíz
 *
 * Configura el enrutamiento y el layout global.
 * Las rutas y páginas se implementan en la Fase 5 (Frontend Dashboard).
 */

import './App.css'

function App() {
  return (
    <div className="app">
      <div className="app__splash">
        <div className="app__logo">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="48" height="48">
            <circle cx="20" cy="20" r="18" stroke="#3b82f6" strokeWidth="2" />
            <circle cx="20" cy="20" r="8" fill="#3b82f6" opacity="0.2" />
            <circle cx="20" cy="20" r="4" fill="#3b82f6" />
            <path d="M20 6 L20 2 M20 38 L20 34 M6 20 L2 20 M38 20 L34 20" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
        <h1 className="app__title">VigilIA</h1>
        <p className="app__subtitle">
          Plataforma de Visión Artificial para SST
        </p>
        <div className="app__status">
          <span className="app__status-dot" />
          <span>Sistema inicializando — Fase 0 completada</span>
        </div>
        <div className="app__phases">
          <div className="app__phase app__phase--done">✓ Fase 0: Fundación</div>
          <div className="app__phase app__phase--next">→ Fase 1: Backend Core</div>
          <div className="app__phase">○ Fase 2: Vision Pipeline</div>
          <div className="app__phase">○ Fase 3: Motor de Reglas</div>
          <div className="app__phase">○ Fase 4: Alertas WebSocket</div>
          <div className="app__phase">○ Fase 5: Dashboard</div>
          <div className="app__phase">○ Fase 6: LLM Reports</div>
        </div>
      </div>
    </div>
  )
}

export default App
