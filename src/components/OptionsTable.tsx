import React from "react";
import type { OptionPosition } from "../types";

interface Props {
  positions: OptionPosition[];
  onChange: (positions: OptionPosition[]) => void;
}

export const OptionsTable: React.FC<Props> = ({ positions, onChange }) => {
  const updateField = (
    id: string,
    field: keyof OptionPosition,
    value: string
  ) => {
    const next = positions.map((p) =>
      p.id === id
        ? {
            ...p,
            [field]:
              field === "symbol" || field === "type" || field === "expiry"
                ? value
                : Number(value)
          }
        : p
    );
    onChange(next);
  };

  const addRow = () => {
    const id = String(Date.now());
    onChange([
      ...positions,
      {
        id,
        symbol: "TICKER",
        underlyingPrice: 100,
        type: "CALL",
        strike: 100,
        expiry: new Date().toISOString().slice(0, 10),
        quantity: 1,
        premium: 1,
        impliedVol: 0.2
      }
    ]);
  };

  const removeRow = (id: string) => {
    onChange(positions.filter((p) => p.id !== id));
  };

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Type</th>
            <th>Strike</th>
            <th>Expiry</th>
            <th>Underlying</th>
            <th>Qty</th>
            <th>Premium</th>
            <th>IV</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {positions.map((p) => (
            <tr key={p.id}>
              <td>
                <input
                  value={p.symbol}
                  onChange={(e) => updateField(p.id, "symbol", e.target.value)}
                />
              </td>
              <td>
                <select
                  value={p.type}
                  onChange={(e) => updateField(p.id, "type", e.target.value)}
                >
                  <option value="CALL">CALL</option>
                  <option value="PUT">PUT</option>
                </select>
              </td>
              <td>
                <input
                  type="number"
                  value={p.strike}
                  onChange={(e) => updateField(p.id, "strike", e.target.value)}
                />
              </td>
              <td>
                <input
                  type="date"
                  value={p.expiry}
                  onChange={(e) => updateField(p.id, "expiry", e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={p.underlyingPrice}
                  onChange={(e) =>
                    updateField(p.id, "underlyingPrice", e.target.value)
                  }
                />
              </td>
              <td>
                <input
                  type="number"
                  value={p.quantity}
                  onChange={(e) =>
                    updateField(p.id, "quantity", e.target.value)
                  }
                />
              </td>
              <td>
                <input
                  type="number"
                  value={p.premium}
                  onChange={(e) =>
                    updateField(p.id, "premium", e.target.value)
                  }
                />
              </td>
              <td>
                <input
                  type="number"
                  min={0}
                  step={0.01}
                  value={p.impliedVol}
                  onChange={(e) =>
                    updateField(p.id, "impliedVol", e.target.value)
                  }
                />
              </td>
              <td>
                <button
                  className="ghost-button"
                  type="button"
                  onClick={() => removeRow(p.id)}
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="primary-button" type="button" onClick={addRow}>
        + Add position
      </button>
    </div>
  );
};


