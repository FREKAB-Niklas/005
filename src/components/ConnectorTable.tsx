import React from 'react';
import { Connector, PIN_COUNTS } from '../types';
import { Plus, Trash2 } from 'lucide-react';

interface Props {
  connectors: Connector[];
  setConnectors: React.Dispatch<React.SetStateAction<Connector[]>>;
}

export default function ConnectorTable({ connectors, setConnectors }: Props) {
  const addConnector = () => {
    const newId = `X${connectors.length + 1}`;
    setConnectors([...connectors, { id: newId, type: '', pinCount: 2 }]);
  };

  const removeConnector = (id: string) => {
    setConnectors(connectors.filter(c => c.id !== id));
  };

  const updateConnector = (id: string, field: keyof Connector, value: string | number) => {
    setConnectors(connectors.map(c => 
      c.id === id ? { ...c, [field]: value } : c
    ));
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              ID
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Type
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Pin Count
            </th>
            <th className="px-6 py-3 bg-gray-50"></th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {connectors.map((connector) => (
            <tr key={connector.id}>
              <td className="px-6 py-4 whitespace-nowrap">
                <input
                  type="text"
                  value={connector.id}
                  onChange={(e) => updateConnector(connector.id, 'id', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <input
                  type="text"
                  value={connector.type}
                  onChange={(e) => updateConnector(connector.id, 'type', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="e.g. DT06-2S"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={connector.pinCount}
                  onChange={(e) => updateConnector(connector.id, 'pinCount', parseInt(e.target.value))}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {PIN_COUNTS.map(count => (
                    <option key={count} value={count}>{count}</option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  onClick={() => removeConnector(connector.id)}
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
          onClick={addConnector}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Connector
        </button>
      </div>
    </div>
  );
}