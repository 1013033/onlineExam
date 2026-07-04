const fs = require('fs');
const path = require('path');

const appData = process.env.APPDATA;
const historyDir = path.join(appData, 'Code', 'User', 'History');
console.log("Searching in:", historyDir);

function walkDir(dir, callback) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      walkDir(fullPath, callback);
    } else if (stat.isFile()) {
      callback(fullPath, stat);
    }
  }
}

let found = 0;
walkDir(historyDir, (filepath, stat) => {
  if (filepath.endsWith('.js') || stat.size > 15000 && stat.size < 25000) {
    try {
      const content = fs.readFileSync(filepath, 'utf8');
      if (content.includes('COURSE') && content.includes('quiz') && content.includes('parse')) {
        console.log(`FOUND BACKUP: ${filepath} (size: ${stat.size} bytes, modified: ${stat.mtime})`);
        found++;
        fs.writeFileSync(`recovered_js_${found}.js`, content, 'utf8');
      }
    } catch (e) {
      // ignore
    }
  }
});

console.log(`Found ${found} backups.`);
