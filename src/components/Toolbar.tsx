import React from "react";

interface Props {
  riskFreeRate: number;
  onRiskFreeRateChange: (v: number) => void;
  positionCount: number;
  totals: { notional: number; premium: number };
}

export const Toolbar: React.FC<Props> = ({
  riskFreeRate,
  onRiskFreeRateChange,
  positionCount,
  totals
}) => {
  return (
    <div className="toolbar">
      <div className="toolbar-group">
        <label className="field">
          <span>Risk-free rate</span>
          <div className="field-inline">
            <input
              type="number"
              step={0.01}
              value={riskFreeRate}
              onChange={(e) => onRiskFreeRateChange(Number(e.target.value))}
            />
            <span className="field-suffix">as decimal (0.03 = 3%)</span>
          </div>
        </label>
      </div>
      <div className="toolbar-group toolbar-metrics">
        <div className="toolbar-chip">
          <span className="chip-label">Positions</span>
          <span className="chip-value">{positionCount}</span>
        </div>
        <div className="toolbar-chip">
          <span className="chip-label">Notional</span>
          <span className="chip-value">
            ${totals.notional.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </span>
        </div>
        <div className="toolbar-chip">
          <span className="chip-label">Net Premium</span>
          <span className="chip-value">
            {totals.premium >= 0 ? "+" : "-"}$
            {Math.abs(totals.premium).toLocaleString(undefined, {
              maximumFractionDigits: 0
            })}
          </span>
        </div>
      </div>
    </div>
  );
};


