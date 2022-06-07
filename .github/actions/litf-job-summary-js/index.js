const core = require("@actions/core");
const github = require("@actions/github");
const artifact = require("@actions/artifact");

const fs = require("fs");

async function run() {
  try {
    const name = core.getInput("artifact-name", { required: true });

    const downloadOptions = {
      createArtifactFolder: true,
    };
    const artifactClient = artifact.create();

    const downloadResponse = await artifactClient.downloadArtifact(
      name,
      ".",
      downloadOptions
    );

    console.log(downloadResponse.downloadPath);
    fs.readdir(downloadResponse.downloadPath, function (err, files) {
      //handling error
      if (err) {
        return console.log("Unable to scan directory: " + err);
      }
      //listing all files using forEach
      files.forEach(function (file) {
        // Do whatever you want to do with the file
        console.log(file);
      });
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
