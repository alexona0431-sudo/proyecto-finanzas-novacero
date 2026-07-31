"use client";

import { useState } from "react";

const historico = [
  { anio: "2023", ventas: 333.28, utilidad: 15.48, liquidez: 1.76, deuda: 54.6, roe: 9.74 },
  { anio: "2024", ventas: 325.58, utilidad: 9.26, liquidez: 1.76, deuda: 51.07, roe: 5.61 },
  { anio: "2025", ventas: 389.48, utilidad: 16.25, liquidez: 1.59, deuda: 61.79, roe: 9.96 },
];

const contextoEconomico = [
  { indicador: "PIB Ecuador 2025", valor: "3,7 %", detalle: "Crecimiento anual · BCE" },
  { indicador: "Inflación anual", valor: "1,65 %", detalle: "Junio 2026 · INEC" },
  { indicador: "Tasa productiva", valor: "6,91 %", detalle: "Julio 2026 · BCE" },
  { indicador: "Empleo adecuado", valor: "37,1 %", detalle: "Diciembre 2025 · INEC" },
];

const flujoHitos = [
  { anio: 0, flujo: -850000, x: 55, y: 230 },
  { anio: 1, flujo: 86062.5, x: 205, y: 52 },
  { anio: 5, flujo: 90519.35, x: 355, y: 51 },
  { anio: 10, flujo: 28450.21, x: 505, y: 63 },
  { anio: 15, flujo: 102806.84, x: 655, y: 48 },
  { anio: 20, flujo: 194618.86, x: 805, y: 31 },
];

const escenarios = {
  Optimista: {
    van: 411392.41,
    tir: 14.21,
    bc: 1.341,
    payback: "6,70 años",
    descontado: "10,30 años",
    clase: "positive",
    decision: "Aceptar",
  },
  Base: {
    van: -66057.81,
    tir: 8.91,
    bc: 0.943,
    payback: "10,07 años",
    descontado: "No recuperado",
    clase: "warning",
    decision: "Rediseñar",
  },
  Pesimista: {
    van: -452381.97,
    tir: 3.83,
    bc: 0.603,
    payback: "15,01 años",
    descontado: "No recuperado",
    clase: "negative",
    decision: "Rechazar",
  },
};

const razones = [
  ["Liquidez corriente", "1,76", "1,76", "1,59", "Disminuyó; aún supera 1"],
  ["Prueba ácida", "0,57", "0,97", "0,76", "Dependencia de inventarios"],
  ["Endeudamiento", "54,60 %", "51,07 %", "61,79 %", "Mayor presión financiera"],
  ["Margen neto", "4,65 %", "2,84 %", "4,17 %", "Recuperación parcial"],
  ["ROA", "4,42 %", "2,74 %", "3,81 %", "Mejora frente a 2024"],
  ["ROE", "9,74 %", "5,61 %", "9,96 %", "Recuperación en 2025"],
  ["Cobertura intereses", "3,38x", "2,29x", "3,50x", "Capacidad aceptable"],
  ["Rotación de activos", "0,95x", "0,95x", "1,02x", "Eficiencia creciente"],
];

const riesgos = [
  ["Generación inferior", "Media", "Alto", "Estudio solar y garantía de rendimiento"],
  ["Sobrecosto de instalación", "Media", "Alto", "Tres cotizaciones y precio fijo"],
  ["Autoconsumo menor", "Media", "Alto", "Validar curvas horarias de carga"],
  ["Cambio de tarifa", "Media", "Alto", "Actualizar sensibilidad anualmente"],
  ["Reemplazo del inversor", "Media", "Medio", "Garantía y fondo de reposición"],
  ["Aumento de tasa", "Baja", "Medio", "Negociar crédito a tasa fija"],
];

const fuentes = [
  ["Superintendencia de Compañías", "Estados financieros de Novacero 2023–2025", "https://www.supercias.gob.ec/portalscvs/index.htm"],
  ["Banco Central del Ecuador", "PIB 2025 y tasa productiva corporativa", "https://www.bce.fin.ec/"],
  ["INEC", "Inflación y empleo", "https://www.ecuadorencifras.gob.ec/"],
  ["ARCONEL", "Pliegos tarifarios eléctricos 2026", "https://arconel.gob.ec/servicio-publico-de-energia-electrica-spee/"],
  ["Novacero", "Memoria de Sostenibilidad 2025", "https://www.novacero.com/"],
];

const dinero = (valor) =>
  new Intl.NumberFormat("es-EC", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(valor);

function Icon({ children }) {
  return <span className="icon" aria-hidden="true">{children}</span>;
}

function MiniBars() {
  const max = Math.max(...historico.map((dato) => dato.ventas));
  return (
    <div className="bar-chart" aria-label="Ventas de Novacero entre 2023 y 2025">
      {historico.map((dato) => (
        <div className="bar-column" key={dato.anio}>
          <div className="bar-value">${dato.ventas.toFixed(1)} M</div>
          <div
            className="bar"
            style={{ height: `${Math.max(24, (dato.ventas / max) * 150)}px` }}
          />
          <strong>{dato.anio}</strong>
        </div>
      ))}
    </div>
  );
}

function CashFlowChart() {
  const puntos = flujoHitos.map((dato) => `${dato.x},${dato.y}`).join(" ");
  return (
    <div className="cashflow-chart">
      <svg viewBox="0 0 860 270" role="img" aria-label="Flujo de caja proyectado del sistema fotovoltaico">
        <defs>
          <linearGradient id="areaFlow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#b8d35d" stopOpacity=".28" />
            <stop offset="100%" stopColor="#b8d35d" stopOpacity="0" />
          </linearGradient>
        </defs>
        <line x1="35" y1="69" x2="830" y2="69" className="zero-line" />
        <text x="36" y="62" className="axis-label">USD 0</text>
        <polyline points={puntos} className="flow-line shadow-line" />
        <polyline points={puntos} className="flow-line" />
        {flujoHitos.map((dato) => (
          <g key={dato.anio}>
            <line x1={dato.x} y1={dato.y} x2={dato.x} y2="244" className="guide-line" />
            <circle cx={dato.x} cy={dato.y} r="6" className={dato.flujo < 0 ? "flow-point negative-point" : "flow-point"} />
            <text x={dato.x} y={dato.y < 45 ? dato.y + 25 : dato.y - 14} textAnchor="middle" className="flow-value">
              {dato.flujo < 0 ? "−$850.000" : `$${Math.round(dato.flujo / 1000)} mil`}
            </text>
            <text x={dato.x} y="262" textAnchor="middle" className="year-label">Año {dato.anio}</text>
          </g>
        ))}
      </svg>
    </div>
  );
}

function App() {
  const [escenario, setEscenario] = useState("Base");
  const actual = escenarios[escenario];

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#inicio" aria-label="Inicio">
          <span className="brand-mark">N</span>
          <span>
            <strong>NOVACERO</strong>
            <small>Inteligencia financiera</small>
          </span>
        </a>
        <nav aria-label="Navegación principal">
          <a href="#diagnostico">Diagnóstico</a>
          <a href="#inversion">Inversión</a>
          <a href="#riesgos">Riesgos</a>
          <a href="#valoracion">Valoración</a>
        </nav>
        <div className="updated"><span /> Actualizado 30 jul 2026</div>
      </header>

      <section className="hero" id="inicio">
        <div className="hero-copy">
          <div className="eyebrow">Proyecto integrador · Ingeniería económica</div>
          <h1>Decidir con datos.<br /><span>Invertir con criterio.</span></h1>
          <p>
            Evaluación de una ampliación fotovoltaica de <strong>1.000 kWp</strong> en
            la planta Lasso de Novacero, comparando recursos propios, crédito bancario
            y la alternativa de no invertir.
          </p>
          <div className="hero-actions">
            <a className="button primary" href="#inversion">Ver evaluación</a>
            <a className="button ghost" href="#metodologia">Consultar metodología</a>
          </div>
        </div>
        <div className="decision-panel">
          <div className="decision-top">
            <span>DECISIÓN DEL ESCENARIO BASE</span>
            <span className="status warning">REDISEÑAR</span>
          </div>
          <div className="decision-number">VAN {dinero(-66057.81)}</div>
          <p>La rentabilidad base no alcanza el rendimiento mínimo requerido.</p>
          <div className="threshold">
            <div>
              <span>Inversión máxima viable</span>
              <strong>$785.852</strong>
            </div>
            <div>
              <span>Tarifa mínima</span>
              <strong>$0,0919/kWh</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="metrics-strip" aria-label="Indicadores principales">
        <article><Icon>↘</Icon><span>VAN BASE</span><strong className="red">−$66.058</strong><small>Destruye valor con los supuestos actuales</small></article>
        <article><Icon>↗</Icon><span>TIR</span><strong>8,91 %</strong><small>Inferior a la tasa mínima del 10 %</small></article>
        <article><Icon>◎</Icon><span>WACC</span><strong>7,38 %</strong><small>Costo ponderado del financiamiento</small></article>
        <article><Icon>◫</Icon><span>BENEFICIO / COSTO</span><strong>0,943</strong><small>Menor que 1 en el escenario base</small></article>
      </section>

      <section className="economic-context" aria-label="Entorno económico">
        <div className="context-intro">
          <span>ENTORNO ECONÓMICO</span>
          <strong>Ecuador · 2025–2026</strong>
        </div>
        {contextoEconomico.map((dato) => (
          <article key={dato.indicador}>
            <span>{dato.indicador}</span>
            <strong>{dato.valor}</strong>
            <small>{dato.detalle}</small>
          </article>
        ))}
      </section>

      <section className="section" id="diagnostico">
        <div className="section-heading">
          <div><span className="section-number">01</span><h2>Diagnóstico financiero</h2></div>
          <p>Estados financieros públicos presentados ante la Superintendencia de Compañías.</p>
        </div>

        <div className="grid two">
          <article className="card chart-card">
            <div className="card-title">
              <div><span>VENTAS</span><h3>Evolución de ingresos</h3></div>
              <span className="tag positive">+19,6 % en 2025</span>
            </div>
            <MiniBars />
            <p className="insight"><strong>Lectura:</strong> las ventas se recuperaron en 2025 y superaron los niveles de los dos años anteriores.</p>
          </article>
          <article className="card balance-card">
            <div className="card-title">
              <div><span>ESTRUCTURA 2025</span><h3>Solidez y presión financiera</h3></div>
            </div>
            <div className="donut-row">
              <div className="donut"><div><strong>61,79 %</strong><span>Deuda</span></div></div>
              <div className="balance-list">
                <div><span>Activo total</span><strong>$426,65 M</strong></div>
                <div><span>Pasivo total</span><strong>$263,61 M</strong></div>
                <div><span>Patrimonio</span><strong>$163,04 M</strong></div>
                <div><span>Flujo operativo</span><strong className="red">−$21,36 M</strong></div>
              </div>
            </div>
            <p className="insight"><strong>Alerta:</strong> el aumento del pasivo y el flujo operativo negativo limitan la capacidad de asumir inversiones sin validación adicional.</p>
          </article>
        </div>

        <article className="card table-card">
          <div className="card-title">
            <div><span>RAZONES FINANCIERAS</span><h3>Liquidez, eficiencia y rentabilidad</h3></div>
            <span className="source-chip">Datos auditados</span>
          </div>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Indicador</th><th>2023</th><th>2024</th><th>2025</th><th>Interpretación</th></tr></thead>
              <tbody>
                {razones.map((fila) => (
                  <tr key={fila[0]}>{fila.map((celda, index) => <td key={index}>{celda}</td>)}</tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>
      </section>

      <section className="section dark-section" id="inversion">
        <div className="section-heading light">
          <div><span className="section-number">02</span><h2>Ingeniería económica</h2></div>
          <p>Selecciona un escenario para explorar cómo cambia la decisión.</p>
        </div>

        <div className="scenario-tabs" role="tablist" aria-label="Escenarios">
          {Object.keys(escenarios).map((nombre) => (
            <button
              type="button"
              role="tab"
              aria-selected={escenario === nombre}
              className={escenario === nombre ? "active" : ""}
              onClick={() => setEscenario(nombre)}
              key={nombre}
            >
              {nombre}
            </button>
          ))}
        </div>

        <div className="scenario-grid">
          <article className="scenario-main">
            <span className={`status ${actual.clase}`}>{actual.decision.toUpperCase()}</span>
            <small>VALOR ACTUAL NETO</small>
            <strong className={actual.van < 0 ? "red" : "green"}>{dinero(actual.van)}</strong>
            <p>{escenario === "Base"
              ? "El diseño actual necesita menor inversión, mayor autoconsumo o una tarifa evitada superior."
              : escenario === "Optimista"
                ? "La combinación favorable de costos y generación crea valor para la empresa."
                : "La caída de generación y el aumento de costos destruyen valor significativamente."}</p>
          </article>
          <article className="scenario-stat"><span>TIR</span><strong>{actual.tir.toFixed(2)} %</strong><small>Rentabilidad interna</small></article>
          <article className="scenario-stat"><span>B/C</span><strong>{actual.bc.toFixed(3)}</strong><small>Beneficio por dólar de costo</small></article>
          <article className="scenario-stat"><span>Payback</span><strong>{actual.payback}</strong><small>Recuperación simple</small></article>
          <article className="scenario-stat"><span>Descontado</span><strong>{actual.descontado}</strong><small>Recuperación con descuento</small></article>
        </div>

        <article className="card dark-card cashflow-card">
          <div className="card-title">
            <div><span>FLUJO DE CAJA PROYECTADO</span><h3>Horizonte de evaluación: 20 años</h3></div>
            <span className="source-chip dark-chip">Modelo reproducible</span>
          </div>
          <CashFlowChart />
          <div className="cashflow-notes">
            <div><span>Inversión inicial</span><strong className="red">−$850.000</strong><small>Año 0</small></div>
            <div><span>Flujo operativo inicial</span><strong>$86.063</strong><small>Año 1</small></div>
            <div><span>Reemplazo del inversor</span><strong>$28.450</strong><small>Flujo neto del año 10</small></div>
            <div><span>Flujo final</span><strong>$194.619</strong><small>Año 20, incluye valor residual</small></div>
          </div>
          <p className="note"><strong>Interpretación:</strong> el proyecto genera flujos positivos después del desembolso inicial, pero su valor descontado no alcanza a recuperar la inversión bajo los supuestos base.</p>
        </article>

        <div className="grid two finance-grid">
          <article className="card dark-card">
            <div className="card-title"><div><span>FINANCIAMIENTO</span><h3>Comparación de alternativas</h3></div></div>
            <div className="finance-option"><div><span>Recursos propios</span><small>100 % patrimonio</small></div><strong>VAN −$189.838</strong></div>
            <div className="finance-option selected"><div><span>Crédito bancario</span><small>70 % deuda · 30 % propio</small></div><strong>VAN −$85.701</strong></div>
            <div className="finance-option"><div><span>No invertir</span><small>Sin desembolso</small></div><strong>VAN $0</strong></div>
            <p className="note">Aunque el crédito mejora el VAN del inversionista, ninguna alternativa de inversión base crea valor.</p>
          </article>
          <article className="card dark-card">
            <div className="card-title"><div><span>PUNTOS DE EQUILIBRIO</span><h3>Condiciones para alcanzar VAN = 0</h3></div></div>
            <div className="break-even"><span>Tarifa evitada</span><div><i style={{width:"84%"}} /></div><strong>$0,0919/kWh</strong></div>
            <div className="break-even"><span>Inversión máxima</span><div><i style={{width:"76%"}} /></div><strong>$785.852</strong></div>
            <div className="break-even"><span>Autoconsumo mínimo</span><div><i style={{width:"97%"}} /></div><strong>97,35 %</strong></div>
            <p className="note">Estos límites orientan la negociación con proveedores y la validación técnica previa.</p>
          </article>
        </div>
      </section>

      <section className="section" id="valoracion">
        <div className="section-heading">
          <div><span className="section-number">03</span><h2>Valoración empresarial</h2></div>
          <p>Un método principal y un contraste para evitar depender de una sola estimación.</p>
        </div>
        <div className="valuation-grid">
          <article className="valuation-card primary-value">
            <span>MÉTODO PRINCIPAL · FCFE</span>
            <strong>$96,75 M</strong>
            <p>Flujo normalizado equivalente al 70 % de la utilidad promedio, crecimiento explícito de 3 % y costo del patrimonio de 12,5 %.</p>
          </article>
          <div className="versus">VS</div>
          <article className="valuation-card">
            <span>CONTRASTE · VALOR CONTABLE AJUSTADO</span>
            <strong>$144,99 M</strong>
            <p>Patrimonio 2025 ajustado conservadoramente por inventarios y cuentas por cobrar.</p>
          </article>
        </div>
        <div className="policy">
          <div><Icon>◆</Icon><h3>Política propuesta</h3></div>
          <p>Retener inicialmente el <strong>70 % de las utilidades</strong> y distribuir hasta 30 %, sujeto a flujo operativo positivo, liquidez superior a 1,50 y cumplimiento de obligaciones financieras.</p>
        </div>
      </section>

      <section className="section risk-section" id="riesgos">
        <div className="section-heading">
          <div><span className="section-number">04</span><h2>Riesgos y controles</h2></div>
          <p>La sostenibilidad no sustituye la disciplina financiera.</p>
        </div>
        <div className="risk-list">
          {riesgos.map((riesgo) => (
            <article key={riesgo[0]}>
              <div className={`risk-dot ${riesgo[2].toLowerCase()}`} />
              <div><strong>{riesgo[0]}</strong><small>Probabilidad {riesgo[1]} · Impacto {riesgo[2]}</small></div>
              <p>{riesgo[3]}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section method-section" id="metodologia">
        <div className="section-heading">
          <div><span className="section-number">05</span><h2>Metodología y trazabilidad</h2></div>
          <p>Cálculos reproducibles, fuentes citadas y supuestos identificados.</p>
        </div>
        <div className="method-grid">
          <article><Icon>01</Icon><strong>Datos reales</strong><p>Estados financieros oficiales 2023–2025.</p></article>
          <article><Icon>02</Icon><strong>Validación</strong><p>18 igualdades contables comprobadas.</p></article>
          <article><Icon>03</Icon><strong>Modelación</strong><p>Flujos, WACC, VAN, TIR y valoración mediante código.</p></article>
          <article><Icon>04</Icon><strong>Riesgo</strong><p>Tres escenarios, sensibilidad y puntos de equilibrio.</p></article>
        </div>
        <div className="sources">
          <h3>Fuentes verificables</h3>
          {fuentes.map(([entidad, detalle, url]) => (
            <a href={url} target="_blank" rel="noreferrer" key={entidad}>
              <span><strong>{entidad}</strong><small>{detalle}</small></span><b>↗</b>
            </a>
          ))}
        </div>
      </section>

      <section className="final-recommendation">
        <div>
          <span className="eyebrow">RECOMENDACIÓN EJECUTIVA</span>
          <h2>No invertir todavía.<br /><span>Negociar, validar y rediseñar.</span></h2>
        </div>
        <p>
          La ampliación fotovoltaica es coherente con la estrategia ambiental de Novacero,
          pero el escenario base no crea valor. Se recomienda solicitar cotizaciones reales,
          revisar doce meses de consumo horario y aprobar únicamente un diseño que alcance
          VAN positivo y mantenga controlado el endeudamiento.
        </p>
      </section>

      <footer>
        <div className="brand"><span className="brand-mark">N</span><span><strong>NOVACERO</strong><small>Proyecto académico independiente</small></span></div>
        <p>Datos reales y supuestos académicos claramente identificados.</p>
        <span>Actualizado: 30 de julio de 2026</span>
      </footer>
    </main>
  );
}

export default App;
