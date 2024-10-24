import React from 'react';
import { Splice } from '../types';
import { Plus, Trash2 } from 'lucide-react';

interface Props {
  splices: Splice[];
  setSplices: React.Dispatch<React.SetStateAction<Splice[]>>;
}

export default function SpliceTable({ splices, setSplices }: Props) {
  const addSplice = () => {
    const newId = `SP${splices.length + 1}`;
    setSplices([...splices, { id: newId }]);
  };

  const removeSplice = (id: string) => {
    setSplices(splices.filter(s => s.id !== id));
  };

  const updateSplice = (id: string, newId: string) => {
    setSplices(splices.map(s => 
      s.id === id ? { ...s, id: newId } : s
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
            <th className="px-6 py-3 bg-gray-50"></th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {splices.map((splice) => (
            <tr key={splice.id}>
              <td className="px-6 py-4 whitespace-nowrap">
                <input
                  type="text"
                  value={splice.id}
                  onChange={(e) => updateSplice(splice.id, e.target.value)}
                  className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="e.g. SP1"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  onClick={() => removeSplice(splice.id)}
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
          onClick={addSplice}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Splice
        </button>
      </div>
    </div>
  );
}