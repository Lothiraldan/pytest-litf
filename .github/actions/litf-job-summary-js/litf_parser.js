const fs = require("fs");
const os = require("os");

function parseLitfJSONLFile(filePath) {
  let fileContent = fs.readFileSync(filePath, { encoding: "utf-8" });
  let data = fileContent
    // Split on new line
    .split(os.EOL)
    // Remove blank lines
    .filter((p) => p.trim())
    // Parse the JSON
    .map(JSON.parse);

  return data;
}

exports.parseLitfJSONLFile = parseLitfJSONLFile;

if (require.main === module) {
  console.log(parseLitfJSONLFile(process.argv[2]));
}
