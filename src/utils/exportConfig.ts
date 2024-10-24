export function exportToText(
  connectors: { id: string; type: string; pinCount: number }[],
  splices: { id: string }[],
  cables: { id: string; color: string; gaugeType: string; gauge: string; length: number }[],
  connections: { id: string; wireId: string; fromConnector: string; fromPin: number; toConnector: string; toPin: number }[]
): string {
  let output = '';

  // Export Connectors and Splices
  output += 'connectors:\n';
  connectors.forEach(connector => {
    output += `  ${connector.id}:\n`;
    output += `    type: ${connector.type}\n`;
    output += `    pincount: ${connector.pinCount}\n`;
  });
  splices.forEach(splice => {
    output += `  ${splice.id}:\n`;
    output += `    style: simple\n`;
    output += `    type: splice\n`;
  });
  output += '\n';

  // Export Cables
  output += 'cables:\n';
  cables.forEach(cable => {
    output += `  ${cable.id}:\n`;
    const gauge = cable.gaugeType === 'AWG' 
      ? convertAWGtoMM2(cable.gauge)
      : cable.gauge.replace('mm²', ' mm2');
    output += `    gauge: ${gauge}\n`;
    output += `    length: ${cable.length}\n`;
    output += `    color: ${cable.color}\n`;
    output += `    wirecount: 1\n`;
  });
  output += '\n';

  // Export Connections
  output += 'connections:\n';
  connections.forEach(connection => {
    output += '  -\n';
    output += `    - ${connection.fromConnector}: [${connection.fromPin}]\n`;
    output += `    - ${connection.wireId}: [${connection.fromPin}]\n`;
    output += `    - ${connection.toConnector}: [${connection.toPin}]\n`;
  });

  return output;
}

// Helper function to convert AWG to mm²
function convertAWGtoMM2(awg: string): string {
  const awgToMM2: { [key: string]: string } = {
    'AWG30': '0.05 mm2',
    'AWG28': '0.08 mm2',
    'AWG26': '0.14 mm2',
    'AWG24': '0.25 mm2',
    'AWG22': '0.34 mm2',
    'AWG20': '0.5 mm2',
    'AWG18': '0.75 mm2',
    'AWG16': '1.5 mm2', // Updated to correct value
    'AWG14': '2.5 mm2',
    'AWG12': '4.0 mm2',
    'AWG10': '6.0 mm2',
    'AWG8': '10.0 mm2',
    'AWG6': '16.0 mm2',
    'AWG4': '25.0 mm2',
    'AWG2': '35.0 mm2',
    'AWG1': '50.0 mm2'
  };
  return awgToMM2[awg] || '0.75 mm2';
}

export function downloadTextFile(content: string, filename: string) {
  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}