const core = require("@actions/core");
const github = require("@actions/github");
const artifact = require("@actions/artifact");
const glob = require("glob");
const path = require("node:path");
const fs = require("fs");
const os = require("os");
const litf_parser = require("./litf_parser");

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

    let totalSummary = {
      total_duration: 0,
      passed: 0,
      failed: 0,
      error: 0,
      skipped: 0,
    };
    let summaryTable = [
      [
        { data: "File", header: true },
        { data: "Duration", header: true },
        { data: "Passed", header: true },
        { data: "Failed", header: true },
        { data: "Error", header: true },
        { data: "Skipped", header: true },
      ],
    ];

    for (filePath of matchingFiles) {
      let data = litf_parser.parseLitfJSONLFile(filePath);

      // Add data to the table
      summaryTable.push([
        filePath, // TODO: Support naming?
        data.summary.total_duration,
        data.summary.passed,
        data.summary.failed,
        data.summary.error,
        data.summary.skipped,
      ]);

      // Update total summary
      totalSummary.total_duration += data.summary.total_duration;
      totalSummary.passed += data.summary.passed;
      totalSummary.failed += data.summary.failed;
      totalSummary.error += data.summary.error;
      totalSummary.skipped += data.summary.skipped;

      console.log(`File ${filePath}`);
      console.log(data);
    }

    summaryTable.push([
      "**Total**",
      totalSummary.total_duration,
      totalSummary.passed,
      totalSummary.failed,
      totalSummary.error,
      totalSummary.skipped,
    ]);

    await core.summary
      .addHeading("Test Summary")
      .addRaw(`Number of files: ${matchingFiles.length}`)
      .addTable(summaryTable)
      .write();
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
