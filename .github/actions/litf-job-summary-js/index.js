const core = require("@actions/core");
const github = require("@actions/github");
const artifact = require("@actions/artifact");
const glob = require("glob");
const path = require("node:path");

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

    const matchingFiles = glob.sync(
      path.join(downloadResponse.downloadPath, "*.litf.jsonl")
    );

    await core.summary
      .addHeading("Test Summary")
      .addRaw(`Number of files: ${matchingFiles.length}`)
      .write();
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
