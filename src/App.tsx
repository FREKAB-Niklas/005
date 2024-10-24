import React, { useState } from 'react';
import { Cable, Download, Plug, Settings, Archive } from 'lucide-react';
import ConnectorTable from './components/ConnectorTable';
import SpliceTable from './components/SpliceTable';
import CableTable from './components/CableTable';
import ConnectionTable from './components/ConnectionTable';
import VisualBuilder from './components/VisualBuilder';
import WirevizPreview from './components/WirevizPreview';
import { Connector, Splice, CableWire, Connection } from './types';
import { exportToText, downloadTextFile } from './utils/exportConfig';
import { downloadProject } from './utils/downloadProject';

function App() {
  const [activeTab, setActiveTab] = useState<'spreadsheet' | 'visual'>('spreadsheet');
  const [connectors, setConnectors] = useState<Connector[]>([]);
  const [splices, setSplices] = useState<Splice[]>([]);
  const [cables, setCables] = useState<CableWire[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);

  const handleExport = () => {
    const content = exportToText(connectors, splices, cables, connections);
    downloadTextFile(content, 'cable-config.txt');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Cable className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Cable Configurator</h1>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={downloadProject}
                className="px-4 py-2 rounded-md flex items-center space-x-2 text-gray-600 hover:bg-gray-100"
              >
                <Archive className="h-5 w-5" />
                <span>Download Project</span>
              </button>
              <button
                onClick={handleExport}
                className="px-4 py-2 rounded-md flex items-center space-x-2 text-gray-600 hover:bg-gray-100"
              >
                <Download className="h-5 w-5" />
                <span>Export Config</span>
              </button>
              <button
                onClick={() => setActiveTab('spreadsheet')}
                className={`px-4 py-2 rounded-md flex items-center space-x-2 ${
                  activeTab === 'spreadsheet'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Settings className="h-5 w-5" />
                <span>Spreadsheet View</span>
              </button>
              <button
                onClick={() => setActiveTab('visual')}
                className={`px-4 py-2 rounded-md flex items-center space-x-2 ${
                  activeTab === 'visual'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Plug className="h-5 w-5" />
                <span>Visual Builder</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          <div className="w-1/2">
            {activeTab === 'spreadsheet' ? (
              <div className="space-y-8">
                <section className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-lg font-semibold mb-4">Connectors</h2>
                  <ConnectorTable
                    connectors={connectors}
                    setConnectors={setConnectors}
                  />
                </section>

                <section className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-lg font-semibold mb-4">Splices</h2>
                  <SpliceTable
                    splices={splices}
                    setSplices={setSplices}
                  />
                </section>

                <section className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-lg font-semibold mb-4">Cables</h2>
                  <CableTable
                    cables={cables}
                    setCables={setCables}
                  />
                </section>

                <section className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-lg font-semibold mb-4">Connections</h2>
                  <ConnectionTable
                    connections={connections}
                    setConnections={setConnections}
                    connectors={connectors}
                    cables={cables}
                    splices={splices}
                  />
                </section>
              </div>
            ) : (
              <VisualBuilder
                connectors={connectors}
                cables={cables}
                connections={connections}
                setConnectors={setConnectors}
                setCables={setCables}
                setConnections={setConnections}
              />
            )}
          </div>

          <div className="w-1/2 space-y-8">
            <WirevizPreview
              connectors={connectors}
              splices={splices}
              cables={cables}
              connections={connections}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;