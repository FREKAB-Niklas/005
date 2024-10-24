import React, { useState } from 'react';
import { Connector, Splice, CableWire, Connection } from '../types';
import { exportToText } from '../utils/exportConfig';

interface Props {
  connectors: Connector[];
  splices: Splice[];
  cables: CableWire[];
  connections: Connection[];
}

export default function WirevizPreview({ connectors, splices, cables, connections }: Props) {
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const yamlConfig = exportToText(connectors, splices, cables, connections);

  const handleGenerateDiagram = async () => {
    setGenerating(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:3000/api/generate-diagram', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ yaml: yamlConfig }),
      });
      
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Failed to generate diagram');
      }
      
      setImageUrl(data.imageUrl);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Wireviz Preview</h2>
          <button
            onClick={handleGenerateDiagram}
            disabled={generating}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {generating ? 'Generating...' : 'Generate Diagram'}
          </button>
        </div>

        {error && (
          <div className="p-4 bg-red-50 text-red-700 rounded-md mb-4">
            {error}
          </div>
        )}

        <div className="font-mono text-sm bg-gray-50 p-4 rounded-md overflow-x-auto">
          <pre>{yamlConfig}</pre>
        </div>

        {imageUrl && (
          <div className="mt-4">
            <img 
              src={imageUrl} 
              alt="Wireviz Diagram" 
              className="max-w-full h-auto"
            />
          </div>
        )}
      </div>
    </div>
  );
}