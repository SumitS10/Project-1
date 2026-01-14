import React, { useMemo } from "react";
import type { OptionPosition } from "../types";

interface Props {
  positions: OptionPosition[];
  riskFreeRate: number;
}

// Very simplified Black-Scholes delta approximation for demonstration purposes.
function approximateDelta(position: OptionPosition): number {
  const moneyness =
    (position.underlyingPrice - position.strike) / position.underlyingPrice;
  const sign = position.type === "CALL" ? 1 : -1;
  const base = Math.max(-1, Math.min(1, moneyness * 4));
  return sign * base * position.quantity * 100;
}

export const RiskSummary: React.FC<Props> = ({ positions, riskFreeRate }) => {
  const stats = useMemo(() => {
    const today = new Date();
    let totalDelta = 0;
    let totalPremium = 0;
    let worstCasePnL = 0;

    positions.forEach((p) => {
      const delta = approximateDelta(p);
      totalDelta += delta;

      const premium = p.premium * p.quantity * 100;
      totalPremium += premium;

      const expiryDate = new Date(p.expiry);
      const daysToExp = Math.max(
        0,
        (expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
      );

      const move = p.underlyingPrice * 0.15; // +/- 15% shock
      const intrinsicDown =
        p.type === "CALL"
          ? Math.max(0, p.underlyingPrice - move - p.strike)
          : Math.max(0, p.strike - (p.underlyingPrice - move));
      const intrinsicUp =
        p.type === "CALL"
          ? Math.max(0, p.underlyingPrice + move - p.strike)
          : Math.max(0, p.strike - (p.underlyingPrice + move));

      const payoffDown = intrinsicDown * p.quantity * 100;
      const payoffUp = intrinsicUp * p.quantity * 100;

      const scenarioPnL = Math.min(payoffDown, payoffUp) - premium;
      worstCasePnL += scenarioPnL;

      // eslint-disable-next-line no-console
      if (Number.isNaN(daysToExp)) {
        // keep example simple; ignore NaNs
      }
    });

    return {
      totalDelta,
      totalPremium,
      worstCasePnL
    };
  }, [positions]);

  return (
    <div className="risk-grid">
      <div className="risk-card">
        <h3>Total Delta</h3>
        <p className="metric">{stats.totalDelta.toFixed(0)}</p>
        <p className="metric-caption">
          Approximate delta exposure in shares (all positions).
        </p>
      </div>
      <div className="risk-card">
        <h3>Net Premium</h3>
        <p
          className={`metric ${
            stats.totalPremium >= 0 ? "metric-positive" : "metric-negative"
          }`}
        >
          {stats.totalPremium >= 0 ? "+" : "-"}$
          {Math.abs(stats.totalPremium).toFixed(0)}
        </p>
        <p className="metric-caption">
          Cash paid/received for all option positions.
        </p>
      </div>
      <div className="risk-card">
        <h3>Stress P/L (±15%)</h3>
        <p
          className={`metric ${
            stats.worstCasePnL >= 0 ? "metric-positive" : "metric-negative"
          }`}
        >
          {stats.worstCasePnL >= 0 ? "+" : "-"}$
          {Math.abs(stats.worstCasePnL).toFixed(0)}
        </p>
        <p className="metric-caption">
          Hypothetical worst case P/L if each underlying moves ±15%.
        </p>
      </div>
      <div className="risk-card">
        <h3>Risk-Free Rate</h3>
        <p className="metric">{(riskFreeRate * 100).toFixed(2)}%</p>
        <p className="metric-caption">
          Used as an input to your risk assumptions (configurable above).
        </p>
      </div>
    </div>
  );
};


