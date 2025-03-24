// Simple server to serve the bundled app in production/gamma environments
const http = require('http');
const fs = require('fs');
const path = require('path');

const port = process.env.PORT || 3000;
const appEnv = process.env.APP_ENV || 'production';

console.log(`Starting server in ${appEnv} environment on port ${port}`);

const server = http.createServer((req, res) => {
  // Serve the bundled app
  if (req.url === '/' || req.url === '/index.html') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>LifeFlow Mobile - ${appEnv.toUpperCase()}</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
            .environment { 
              display: inline-block; 
              padding: 5px 10px; 
              border-radius: 4px; 
              margin-bottom: 20px;
              color: white;
              font-weight: bold;
            }
            .dev { background-color: #28a745; }
            .gamma { background-color: #ffc107; color: black; }
            .production { background-color: #dc3545; }
          </style>
        </head>
        <body>
          <h1>LifeFlow Mobile</h1>
          <div class="environment ${appEnv}">${appEnv.toUpperCase()}</div>
          <p>This is a placeholder for the bundled React Native app.</p>
          <p>API URL: ${process.env.API_URL || 'Not configured'}</p>
        </body>
      </html>
    `);
    return;
  }

  // Serve the bundled JS if requested
  if (req.url === '/main.jsbundle') {
    const bundlePath = path.join(__dirname, '../ios/main.jsbundle');
    
    if (fs.existsSync(bundlePath)) {
      const jsBundle = fs.readFileSync(bundlePath);
      res.writeHead(200, {'Content-Type': 'application/javascript'});
      res.end(jsBundle);
    } else {
      res.writeHead(404, {'Content-Type': 'text/plain'});
      res.end('Bundle not found');
    }
    return;
  }

  // Default 404 response
  res.writeHead(404, {'Content-Type': 'text/plain'});
  res.end('Not found');
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
}); 