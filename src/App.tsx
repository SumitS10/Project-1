import React, { useMemo, useState } from "react";
import { OptionsTable } from "./components/OptionsTable";
import { RiskSummary } from "./components/RiskSummary";
import { Toolbar } from "./components/Toolbar";
import type { OptionPosition } from "./types";

const sampleData: OptionPosition[] = [
  {
    id: "1",
    symbol: "AAPL",
    underlyingPrice: 195,
    type: "CALL",
    strike: 190,
    expiry: "2025-03-21",
    quantity: 10,
    premium: 6.5,
    impliedVol: 0.28
  },
  {
    id: "2",
    symbol: "AAPL",
    underlyingPrice: 195,
    type: "PUT",
    strike: 185,
    expiry: "2025-03-21",
    quantity: -5,
    premium: 4.2,
    impliedVol: 0.3
  },
  {
    id: "3",
    symbol: "SPY",
    underlyingPrice: 485,
    type: "CALL",
    strike: 500,
    expiry: "2025-06-20",
    quantity: 3,
    premium: 9.1,
    impliedVol: 0.22
  }
];

export const App: React.FC = () => {
  const [positions, setPositions] = useState<OptionPosition[]>(sampleData);
  const [riskFreeRate, setRiskFreeRate] = useState(0.03);

  const totals = useMemo(() => {
    const notional = positions.reduce(
      (acc, p) => acc + p.underlyingPrice * Math.abs(p.quantity) * 100,
      0
    );
    const premium = positions.reduce(
      (acc, p) => acc + p.premium * p.quantity * 100,
      0
    );
    return { notional, premium };
  }, [positions]);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Options Tracking & Risk Dashboard</h1>
          <p className="subtitle">
            Track listed options positions and view portfolio-level risk
            metrics.
          </p>
        </div>
      </header>

      <Toolbar
        riskFreeRate={riskFreeRate}
        onRiskFreeRateChange={setRiskFreeRate}
        positionCount={positions.length}
        totals={totals}
      />

      <main className="app-main">
        <section className="panel">
          <div className="panel-header">
            <h2>Positions</h2>
            <span className="badge">{positions.length} active</span>
          </div>
          <OptionsTable positions={positions} onChange={setPositions} />
        </section>

        <section className="panel">
          <div className="panel-header">
            <h2>Risk</h2>
          </div>
          <RiskSummary positions={positions} riskFreeRate={riskFreeRate} />
        </section>
      </main>

      <footer className="app-footer">
        <span>Deploy as a static site via `npm run build` → `dist/`.</span>
      </footer>
    </div>
  );
};


