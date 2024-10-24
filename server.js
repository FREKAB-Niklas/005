import express from 'express';
import path from 'path';
import { exec } from 'child_process';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Serve static files (HTML, CSS, JS) from the public directory
app.use('/diagrams', express.static(path.join(__dirname, 'temp')));

// API endpoint for generating Wireviz diagrams
app.post('/api/generate-diagram', async (req, res) => {
  try {
    const { yaml } = req.body;
    const timestamp = Date.now();
    const yamlPath = path.join(__dirname, 'temp', `wireviz_${timestamp}.yml`);
    
    // Ensure temp directory exists
    await fs.mkdir(path.join(__dirname, 'temp'), { recursive: true });
    
    // Save YAML file
    await fs.writeFile(yamlPath, yaml);

    // Generate diagram using wireviz
    exec(`wireviz ${yamlPath}`, async (error, stdout, stderr) => {
      if (error) {
        console.error('Wireviz error:', error);
        return res.status(500).json({
          success: false,
          error: 'Failed to generate diagram'
        });
      }

      if (stderr) {
        console.error('Wireviz stderr:', stderr);
      }

      // The output PNG will be in the same directory as the YAML
      const pngPath = yamlPath.replace('.yml', '.png');
      try {
        await fs.access(pngPath);
        // Return the URL to access the generated image
        res.json({
          success: true,
          imageUrl: `/diagrams/wireviz_${timestamp}.png`,
          output: stdout
        });
      } catch {
        res.status(500).json({
          success: false,
          error: 'Failed to generate diagram'
        });
      }
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Cleanup old files periodically
async function cleanupOldFiles() {
  try {
    const tempDir = path.join(__dirname, 'temp');
    const files = await fs.readdir(tempDir);
    const now = Date.now();
    
    for (const file of files) {
      const filePath = path.join(tempDir, file);
      const stats = await fs.stat(filePath);
      
      // Remove files older than 1 hour
      if (now - stats.mtimeMs > 3600000) {
        await fs.unlink(filePath);
      }
    }
  } catch (error) {
    console.error('Cleanup error:', error);
  }
}

// Run cleanup every hour
setInterval(cleanupOldFiles, 3600000);

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});