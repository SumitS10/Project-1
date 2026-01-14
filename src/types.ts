export type OptionType = "CALL" | "PUT";

export interface OptionPosition {
  id: string;
  symbol: string;
  underlyingPrice: number;
  type: OptionType;
  strike: number;
  expiry: string; // ISO date
  quantity: number; // positive = long, negative = short
  premium: number; // per-contract price
  impliedVol: number; // decimal (0.25 = 25%)
}


