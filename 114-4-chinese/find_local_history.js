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
  try {
    const content = fs.readFileSync(filepath, 'utf8');
    if (content.includes('window.loadCourseData') || content.includes('q_single_pattern')) {
      console.log(`FOUND JS BACKUP: ${filepath} (size: ${stat.size} bytes, modified: ${stat.mtime})`);
      found++;
      if (found <= 5) {
        console.log("Content snippet:\n", content.substring(0, 500));
        // Save the best copy to a backup file
        fs.writeFileSync(`recovered_course_data_${found}.js`, content, 'utf8');
      }
    }
  } catch (e) {
    // ignore
  }
});

console.log(`Found ${found} JS backup files.`);
