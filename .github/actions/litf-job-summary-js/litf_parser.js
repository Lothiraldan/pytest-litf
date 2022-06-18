const fs = require("fs");
const os = require("os");
const assert = require("node:assert");

function JSONParseMap(element) {
  return JSON.parse(element);
}

function parseLitfJSONLFile(filePath) {
  let fileContent = fs.readFileSync(filePath, { encoding: "utf-8" });
  let rawData = Array.from(
    fileContent
      // Split on new line
      .split(os.EOL)
      // Remove blank lines
      .filter((p) => p.trim())
      // Parse the JSON
      .map(JSONParseMap)
  );

  let session_end_message = rawData[rawData.length - 1];

  // TODO: Validate the whole file instead
  assert.strictEqual(session_end_message["_type"], "session_end");
  delete session_end_message._type;

  return { summary: session_end_message, raw: rawData };
}

exports.parseLitfJSONLFile = parseLitfJSONLFile;

if (require.main === module) {
  console.log(parseLitfJSONLFile(process.argv[2]));
}
