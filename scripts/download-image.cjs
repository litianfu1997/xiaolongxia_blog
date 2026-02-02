// Unsplash Image Downloader Script
// Usage: node scripts/download-image.js "keyword" "output-path"

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ACCESS_KEY = 'CcsaX_NrVgu8cb-DXt0RlNXfCFdSgO-7rzN28tUkoZU';

async function downloadImage(keyword, outputPath) {
  const searchUrl = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(keyword)}&per_page=1&client_id=${ACCESS_KEY}`;

  return new Promise((resolve, reject) => {
    https.get(searchUrl, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          
          if (json.results && json.results.length > 0) {
            const imageUrl = json.results[0].urls.regular;
            
            // Download the image
            https.get(imageUrl, (imgRes) => {
              const fileStream = fs.createWriteStream(outputPath);
              imgRes.pipe(fileStream);
              
              fileStream.on('finish', () => {
                fileStream.close();
                console.log(`Image downloaded: ${outputPath}`);
                resolve(outputPath);
              });
              
              fileStream.on('error', (err) => {
                reject(err);
              });
            }).on('error', (err) => {
              reject(err);
            });
          } else {
            reject(new Error('No images found'));
          }
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', (err) => {
      reject(err);
    });
  });
}

// Command line usage
if (require.main === module) {
  const keyword = process.argv[2] || 'technology';
  const outputPath = process.argv[3] || path.join(__dirname, `../public/assets/images/${Date.now()}.jpg`);
  
  downloadImage(keyword, outputPath)
    .then(() => {
      console.log('Download completed successfully!');
      process.exit(0);
    })
    .catch((err) => {
      console.error('Error:', err.message);
      process.exit(1);
    });
}

module.exports = { downloadImage };
