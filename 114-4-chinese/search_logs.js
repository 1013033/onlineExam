const fs = require('fs');

const logPath = 'C:\\Users\\User\\.gemini\\antigravity-cli\\brain\\43ea39c5-1b1e-403a-a23f-2776e863f58c\\.system_generated\\logs\\transcript.jsonl';
if (fs.existsSync(logPath)) {
  const stats = fs.statSync(logPath);
  console.log("Log file size:", stats.size, "bytes");
} else {
  console.log("Log file does not exist.");
}
