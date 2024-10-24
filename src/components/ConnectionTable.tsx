import React from 'react';
import { Connection, Connector, CableWire, Splice } from '../types';
import { Plus, Trash2 } from 'lucide-react';

interface Props {
  connections: Connection[];
  setConnections: React.Dispatch<React.SetStateAction<Connection[]>>;
  connectors: Connector[];
  cables: CableWire[];
  splices: Splice[];
}

export default function ConnectionTable({ connections, setConnections, connectors, cables, splices }: Props) {
  const addConnection = () => {
    const newId = `C${connections.length + 1}`;
    // Find the first unused cable
    const usedCableIds = new Set(connections.map(c => c.wireId));
    const nextCable = cables.find(c => !usedCableIds.has(c.id));
    
    setConnections([
      ...connections,
      {
        id: newId,
        wireId: nextCable?.id || cables[0]?.id || '',
        fromConnector: connectors[0]?.id || '',
        fromPin: 1,
        toConnector: connectors[1]?.id || '',
        toPin: 1,
      },
    ]);
  };

  const removeConnection = (id: string) => {
    setConnections(connections.filter(c => c.id !== id));
  };

  const updateConnection = (id: string, field: keyof Connection, value: string | number) => {
    setConnections(connections.map(c => 
      c.id === id ? { ...c, [field]: value } : c
    ));
  };

  // Combine connectors and splices for the dropdowns
  const endpoints = [
    ...connectors.map(c => ({ id: c.id, type: 'connector', pinCount: c.pinCount })),
    ...splices.map(s => ({ id: s.id, type: 'splice', pinCount: 2 }))
  ];

  // Get available pins for a given endpoint
  const getPinsForEndpoint = (endpointId: string): number[] => {
    const endpoint = endpoints.find(e => e.id === endpointId);
    if (!endpoint) return [1];
    return Array.from({ length: endpoint.pinCount }, (_, i) => i + 1);
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Wire
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              From
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Pin
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              To
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Pin
            </th>
            <th className="px-6 py-3 bg-gray-50"></th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {connections.map((connection) => (
            <tr key={connection.id}>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={connection.wireId}
                  onChange={(e) => updateConnection(connection.id, 'wireId', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {cables.map((cable) => (
                    <option key={cable.id} value={cable.id}>
                      {cable.id}
                    </option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={connection.fromConnector}
                  onChange={(e) => updateConnection(connection.id, 'fromConnector', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {endpoints.map((endpoint) => (
                    <option key={endpoint.id} value={endpoint.id}>
                      {endpoint.id}
                    </option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={connection.fromPin}
                  onChange={(e) => updateConnection(connection.id, 'fromPin', parseInt(e.target.value))}
                  className="w-20 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {getPinsForEndpoint(connection.fromConnector).map((pin) => (
                    <option key={pin} value={pin}>{pin}</option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={connection.toConnector}
                  onChange={(e) => updateConnection(connection.id, 'toConnector', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {endpoints.map((endpoint) => (
                    <option key={endpoint.id} value={endpoint.id}>
                      {endpoint.id}
                    </option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={connection.toPin}
                  onChange={(e) => updateConnection(connection.id, 'toPin', parseInt(e.target.value))}
                  className="w-20 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {getPinsForEndpoint(connection.toConnector).map((pin) => (
                    <option key={pin} value={pin}>{pin}</option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  onClick={() => removeConnection(connection.id)}
                  className="text-red-600 hover:text-red-900"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4">
        <button
          onClick={addConnection}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Connection
        </button>
      </div>
    </div>
  );
}