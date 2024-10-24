import React from 'react';
import { CableWire, WIRE_COLORS, AWG_SIZES, MM2_SIZES } from '../types';
import { Plus, Trash2 } from 'lucide-react';

interface Props {
  cables: CableWire[];
  setCables: React.Dispatch<React.SetStateAction<CableWire[]>>;
}

export default function CableTable({ cables, setCables }: Props) {
  const addCable = () => {
    const newId = `W${cables.length + 1}`;
    setCables([...cables, { id: newId, color: 'BK', gaugeType: 'AWG', gauge: 'AWG16', length: 500 }]);
  };

  const removeCable = (id: string) => {
    setCables(cables.filter(c => c.id !== id));
  };

  const updateCable = (id: string, field: keyof CableWire, value: string | number) => {
    setCables(cables.map(c => {
      if (c.id === id) {
        const updatedCable = { ...c, [field]: value };
        // Reset gauge when gauge type changes
        if (field === 'gaugeType') {
          updatedCable.gauge = value === 'AWG' ? 'AWG16' : '1mm²';
        }
        return updatedCable;
      }
      return c;
    }));
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
              Color
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Gauge Type
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Gauge
            </th>
            <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Length (mm)
            </th>
            <th className="px-6 py-3 bg-gray-50"></th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {cables.map((cable) => (
            <tr key={cable.id}>
              <td className="px-6 py-4 whitespace-nowrap">
                <input
                  type="text"
                  value={cable.id}
                  onChange={(e) => updateCable(cable.id, 'id', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={cable.color}
                  onChange={(e) => updateCable(cable.id, 'color', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {WIRE_COLORS.map(color => (
                    <option key={color.value} value={color.value}>
                      {color.label}
                    </option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={cable.gaugeType}
                  onChange={(e) => updateCable(cable.id, 'gaugeType', e.target.value as 'AWG' | 'mm²')}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="AWG">AWG</option>
                  <option value="mm²">mm²</option>
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select
                  value={cable.gauge}
                  onChange={(e) => updateCable(cable.id, 'gauge', e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  {(cable.gaugeType === 'AWG' ? AWG_SIZES : MM2_SIZES).map(size => (
                    <option key={size} value={size}>{size}</option>
                  ))}
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <input
                  type="number"
                  value={cable.length}
                  onChange={(e) => updateCable(cable.id, 'length', parseInt(e.target.value))}
                  className="w-24 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  min="1"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  onClick={() => removeCable(cable.id)}
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
          onClick={addCable}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Cable
        </button>
      </div>
    </div>
  );
}