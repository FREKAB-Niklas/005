import React from 'react';
import { Connector, CableWire, Connection } from '../types';

interface Props {
  connectors: Connector[];
  cables: CableWire[];
  connections: Connection[];
  setConnectors: React.Dispatch<React.SetStateAction<Connector[]>>;
  setCables: React.Dispatch<React.SetStateAction<CableWire[]>>;
  setConnections: React.Dispatch<React.SetStateAction<Connection[]>>;
}

export default function VisualBuilder({ 
  connectors, 
  cables, 
  connections,
}: Props) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="text-center text-gray-500 py-12">
        Visual builder coming soon! This will provide an interactive way to design your cable assemblies.
        For now, please use the spreadsheet view to configure your cables.
      </div>
    </div>
  );
}