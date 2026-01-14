// API utility functions for backend integration

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export interface FidelityTrade {
  id: number;
  symbol: string;
  trade_date: string;
  option_type: string;
  strike: number;
  expiry: string;
  quantity: number;
  premium: number;
  pnl?: number;
}

export interface TradierTrade {
  id: number;
  symbol: string;
  trade_date: string;
  option_type: string;
  strike: number;
  expiry: string;
  quantity: number;
  premium: number;
  pnl?: number;
}

export interface WebullTrade {
  id: number;
  symbol: string;
  trade_date: string;
  option_type: string;
  strike: number;
  expiry: string;
  quantity: number;
  premium: number;
  pnl?: number;
}

export interface TradeLog {
  id: number;
  trade_id: string;
  source: string;
  trade_date: string;
  close_date: string | null;
  symbol: string;
  strategy: string;
  expiration: string | null;
  strikes: string;
  net_premium: number;
  total_cost: number;
  pl: number;
  pl_percent: number;
  status: string;
  win_loss: string;
  dte: number | null;
  legs: number;
  closed_legs: number;
  open_net: number;
  close_net: number;
}

// Upload CSV files
export async function uploadFidelityCSV(file: File): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload-fidelity/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Upload failed' }));
    throw new Error(error.error || 'Failed to upload Fidelity CSV');
  }
}

export async function uploadTradierCSV(file: File): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload-tradier/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Upload failed' }));
    throw new Error(error.error || 'Failed to upload Tradier CSV');
  }
}

export async function uploadWebullCSV(file: File): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload-webull/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Upload failed' }));
    throw new Error(error.error || 'Failed to upload Webull CSV');
  }
}

// Fetch trades from backend
export async function fetchFidelityTrades(): Promise<FidelityTrade[]> {
  const response = await fetch(`${API_BASE}/fidelity-trades/`);
  if (!response.ok) {
    throw new Error('Failed to fetch Fidelity trades');
  }
  return response.json();
}

export async function fetchTradierTrades(): Promise<TradierTrade[]> {
  const response = await fetch(`${API_BASE}/tradier-trades/`);
  if (!response.ok) {
    throw new Error('Failed to fetch Tradier trades');
  }
  return response.json();
}

export async function fetchWebullTrades(): Promise<WebullTrade[]> {
  const response = await fetch(`${API_BASE}/webull-trades/`);
  if (!response.ok) {
    throw new Error('Failed to fetch Webull trades');
  }
  return response.json();
}

export async function fetchTradeLog(): Promise<TradeLog[]> {
  const response = await fetch(`${API_BASE}/trade-log/`);
  if (!response.ok) {
    throw new Error('Failed to fetch trade log');
  }
  return response.json();
}

// Convert backend trade format to frontend OptionPosition format
import type { OptionPosition } from './types';

export function convertTradeToPosition(
  trade: FidelityTrade | TradierTrade | WebullTrade,
  underlyingPrice?: number
): OptionPosition {
  return {
    id: `trade-${trade.id}`,
    symbol: trade.symbol,
    underlyingPrice: underlyingPrice || 100, // Default if not provided
    type: trade.option_type as 'CALL' | 'PUT',
    strike: trade.strike,
    expiry: trade.expiry,
    quantity: trade.quantity,
    premium: trade.premium,
    impliedVol: 0.2, // Default IV if not in backend
  };
}

// Fetch all trades and convert to positions
export async function fetchAllPositions(): Promise<OptionPosition[]> {
  try {
    const [fidelityTrades, tradierTrades, webullTrades] = await Promise.all([
      fetchFidelityTrades().catch(() => []),
      fetchTradierTrades().catch(() => []),
      fetchWebullTrades().catch(() => []),
    ]);

    const allTrades = [...fidelityTrades, ...tradierTrades, ...webullTrades];
    return allTrades.map((trade) => convertTradeToPosition(trade));
  } catch (error) {
    console.error('Error fetching positions:', error);
    return [];
  }
}

