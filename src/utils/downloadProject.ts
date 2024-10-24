import JSZip from 'jszip';

const PROJECT_FILES = {
  'package.json': true,
  'server.js': true,
  'app.py': true,
  'requirements.txt': true,
  'src/App.tsx': true,
  'src/main.tsx': true,
  'src/types.ts': true,
  'src/index.css': true,
  'src/components/ConnectorTable.tsx': true,
  'src/components/SpliceTable.tsx': true,
  'src/components/CableTable.tsx': true,
  'src/components/ConnectionTable.tsx': true,
  'src/components/VisualBuilder.tsx': true,
  'src/components/WirevizPreview.tsx': true,
  'src/utils/exportConfig.ts': true,
  'tsconfig.json': true,
  'tsconfig.app.json': true,
  'tsconfig.node.json': true,
  'vite.config.ts': true,
  'postcss.config.js': true,
  'tailwind.config.js': true,
  'eslint.config.js': true,
};

export async function downloadProject() {
  const zip = new JSZip();
  
  // Add all project files to the ZIP
  for (const filePath of Object.keys(PROJECT_FILES)) {
    try {
      const response = await fetch(`/${filePath}`);
      if (response.ok) {
        const content = await response.text();
        zip.file(filePath, content);
      }
    } catch (error) {
      console.error(`Error adding ${filePath} to ZIP:`, error);
    }
  }

  // Generate and download the ZIP file
  const blob = await zip.generateAsync({ type: 'blob' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'cable-configurator.zip';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}