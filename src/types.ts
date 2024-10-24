export interface Connector {
  id: string;
  type: string;
  pinCount: number;
}

export interface Splice {
  id: string;
}

export interface CableWire {
  id: string;
  color: string;
  gaugeType: 'AWG' | 'mm²';
  gauge: string;
  length: number;
}

export interface Connection {
  id: string;
  wireId: string;
  fromConnector: string;
  fromPin: number;
  toConnector: string;
  toPin: number;
}

export const WIRE_COLORS = [
  { value: 'BK', label: 'BK - Black' },
  { value: 'WH', label: 'WH - White' },
  { value: 'GN', label: 'GN - Green' },
  { value: 'YE', label: 'YE - Yellow' },
  { value: 'BU', label: 'BU - Blue' },
  { value: 'RD', label: 'RD - Red' },
  { value: 'BN', label: 'BN - Brown' },
  { value: 'OG', label: 'OG - Orange' },
  { value: 'VT', label: 'VT - Violet' },
  { value: 'GY', label: 'GY - Gray' },
  { value: 'PK', label: 'PK - Pink' },
  { value: 'TQ', label: 'TQ - Turquoise' }
];

export const PIN_COUNTS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 24, 26, 30, 32, 36, 40, 42, 48, 50, 64];

export const AWG_SIZES = [
  'AWG30', 'AWG28', 'AWG26', 'AWG24', 'AWG22', 'AWG20', 'AWG18', 'AWG16', 
  'AWG14', 'AWG12', 'AWG10', 'AWG8', 'AWG6', 'AWG4', 'AWG2', 'AWG1'
];

export const MM2_SIZES = [
  '0.05mm²', '0.08mm²', '0.14mm²', '0.25mm²', '0.34mm²', '0.5mm²', '0.75mm²', 
  '1mm²', '1.5mm²', '2.5mm²', '4mm²', '6mm²', '10mm²', '16mm²', '25mm²', '35mm²'
];