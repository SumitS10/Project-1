import React, { useState } from 'react';
import { 
  placeOptionsTrade, 
  calculateStrategyRisk, 
  type OptionsStrategy, 
  type TradeRequest,
  type RiskAnalysis
} from '../api';

export const OptionsTrading: React.FC = () => {
  const [strategy, setStrategy] = useState<OptionsStrategy>('vertical');
  const [symbol, setSymbol] = useState('');
  const [expiry, setExpiry] = useState('');
  const [strikes, setStrikes] = useState<string[]>(['', '']);
  const [quantities, setQuantities] = useState<number[]>([1, 1]);
  const [loading, setLoading] = useState(false);
  const [riskAnalysis, setRiskAnalysis] = useState<RiskAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleStrikeChange = (index: number, value: string) => {
    const newStrikes = [...strikes];
    newStrikes[index] = value;
    setStrikes(newStrikes);
  };

  const handleQuantityChange = (index: number, value: number) => {
    const newQuantities = [...quantities];
    newQuantities[index] = value;
    setQuantities(newQuantities);
  };

  const getStrikeInputs = () => {
    switch (strategy) {
      case 'vertical':
        return 2; // Long strike, short strike
      case 'iron_condor':
        return 4; // Put spread + Call spread
      case 'pmcc':
        return 2; // Long call (LEAPS), short call
      default:
        return 2;
    }
  };

  const analyzeRisk = async () => {
    if (!symbol || !expiry) {
      setError('Symbol and expiry are required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const risk = await calculateStrategyRisk({
        strategy,
        symbol: symbol.toUpperCase(),
        expiry,
        strikes: strikes.filter(s => s).map(Number),
        quantities: quantities.slice(0, strikes.filter(s => s).length),
      });
      setRiskAnalysis(risk);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze risk');
    } finally {
      setLoading(false);
    }
  };

  const executeTrade = async () => {
    if (!symbol || !expiry || !riskAnalysis) {
      setError('Please analyze risk first');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const tradeRequest: TradeRequest = {
        strategy,
        symbol: symbol.toUpperCase(),
        expiry,
        strikes: strikes.filter(s => s).map(Number),
        quantities: quantities.slice(0, strikes.filter(s => s).length),
        action: 'open', // 'open' or 'close'
      };

      const result = await placeOptionsTrade(tradeRequest);
      setSuccess(`Trade executed successfully! Order ID: ${result.order_id}`);
      setRiskAnalysis(null);
      // Reset form
      setSymbol('');
      setExpiry('');
      setStrikes(['', '']);
      setQuantities([1, 1]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to execute trade');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="options-trading">
      <div className="panel-header">
        <h2>Options Trading</h2>
        <span className="badge">Webull API</span>
      </div>

      <div className="trading-form">
        <div className="form-group">
          <label>
            <span>Strategy</span>
            <select
              value={strategy}
              onChange={(e) => {
                setStrategy(e.target.value as OptionsStrategy);
                const numStrikes = getStrikeInputs();
                setStrikes(Array(numStrikes).fill(''));
                setQuantities(Array(numStrikes).fill(1));
              }}
            >
              <option value="vertical">Vertical Spread</option>
              <option value="iron_condor">Iron Condor</option>
              <option value="pmcc">Poor Man's Covered Call (PMCC)</option>
            </select>
          </label>
        </div>

        <div className="form-group">
          <label>
            <span>Symbol</span>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="AAPL"
              maxLength={10}
            />
          </label>
        </div>

        <div className="form-group">
          <label>
            <span>Expiry Date</span>
            <input
              type="date"
              value={expiry}
              onChange={(e) => setExpiry(e.target.value)}
            />
          </label>
        </div>

        <div className="strikes-section">
          <h3>
            {strategy === 'vertical' && 'Strikes (Long, Short)'}
            {strategy === 'iron_condor' && 'Strikes (Put Short, Put Long, Call Long, Call Short)'}
            {strategy === 'pmcc' && 'Strikes (Long Call LEAPS, Short Call)'}
          </h3>
          {Array.from({ length: getStrikeInputs() }).map((_, index) => (
            <div key={index} className="strike-input-group">
              <label>
                <span>Strike {index + 1}</span>
                <input
                  type="number"
                  step="0.5"
                  value={strikes[index] || ''}
                  onChange={(e) => handleStrikeChange(index, e.target.value)}
                  placeholder="e.g., 150"
                />
              </label>
              <label>
                <span>Quantity</span>
                <input
                  type="number"
                  value={quantities[index] || 1}
                  onChange={(e) => handleQuantityChange(index, Number(e.target.value))}
                  min="1"
                />
              </label>
            </div>
          ))}
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="primary-button"
            onClick={analyzeRisk}
            disabled={loading || !symbol || !expiry}
          >
            {loading ? 'Analyzing...' : 'Analyze Risk'}
          </button>
        </div>
      </div>

      {error && (
        <div className="status-message error">
          ⚠️ {error}
        </div>
      )}

      {success && (
        <div className="status-message success">
          ✅ {success}
        </div>
      )}

      {riskAnalysis && (
        <div className="risk-analysis">
          <h3>Risk Analysis</h3>
          <div className="risk-grid">
            <div className="risk-card">
              <h4>Max Profit</h4>
              <p className="metric metric-positive">
                ${riskAnalysis.max_profit?.toLocaleString() || 'N/A'}
              </p>
            </div>
            <div className="risk-card">
              <h4>Max Loss</h4>
              <p className="metric metric-negative">
                ${riskAnalysis.max_loss?.toLocaleString() || 'N/A'}
              </p>
            </div>
            <div className="risk-card">
              <h4>Breakeven</h4>
              <p className="metric">
                {riskAnalysis.breakeven?.map((be: number) => `$${be.toFixed(2)}`).join(' / ') || 'N/A'}
              </p>
            </div>
            <div className="risk-card">
              <h4>Net Premium</h4>
              <p className="metric">
                ${riskAnalysis.net_premium?.toLocaleString() || 'N/A'}
              </p>
            </div>
            <div className="risk-card">
              <h4>Probability of Profit</h4>
              <p className="metric">
                {riskAnalysis.probability_of_profit 
                  ? (riskAnalysis.probability_of_profit * 100).toFixed(1) + '%'
                  : 'N/A'}
              </p>
            </div>
            <div className="risk-card">
              <h4>Risk/Reward Ratio</h4>
              <p className="metric">
                {riskAnalysis.risk_reward_ratio?.toFixed(2) || 'N/A'}
              </p>
            </div>
          </div>

          <div className="trade-actions">
            <button
              type="button"
              className="primary-button"
              onClick={executeTrade}
              disabled={loading}
            >
              {loading ? 'Executing...' : 'Execute Trade'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

