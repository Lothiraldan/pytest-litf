const core = require("@actions/core");
const github = require("@actions/github");
const artifact = require("@actions/artifact");
const yauzl = require("yauzl");

const fs = require("fs");

async function run() {
  try {
    const name = core.getInput("artifact-name", { required: true });

    const downloadOptions = {
      createArtifactFolder: false,
    };
    const artifactClient = artifact.create();

    const downloadResponse = await artifactClient.downloadArtifact(
      name,
      "./litf-outputs.zip",
      downloadOptions
    );

    yauzl.open("./litf-outputs.zip", function (err, zipfile) {
      if (err) throw err;
      zipfile.on("error", function (err) {
        throw err;
      });

      zipfile.on("entry", function (entry) {
        console.log(entry);
        console.log(entry.getLastModDate());
        if (!dumpContents || /\/$/.exec(entry)) {
          return;
        }
        zipfile.openReadStream(entry, function (err, readStream) {
          if (err) {
            throw err;
          }
          readStream.pipe(process.stdout);
        });
      });
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
