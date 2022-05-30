# -*- coding: utf-8 -*-
import os
import tempfile
import time
from typing import Dict
from zipfile import ZipFile

import requests
from github import Github


def get_api_version() -> str:
    return "6.0-preview"


def list_artifacts(
    runtime_url: str, owner: str, repo: str, run_id: str, token: str
) -> dict[str, str]:
    # Copy of https://github.com/actions/toolkit/blob/8263c4d15d3a8616851e9c7762ce46fbb4f8c552/packages/artifact/src/internal/utils.ts#L222
    list_artifacts_url = f"{runtime_url}_apis/pipelines/workflows/{run_id}/artifacts?api-version={get_api_version()}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }

    print("ARTIFACT URL", list_artifacts_url)

    with requests.get(list_artifacts_url, headers=headers) as response:
        response.raise_for_status()

        return response.json()


class ArtifactNotFoundException(Exception):
    pass


def filter_artifacts(workflow_artifacts: Dict[str, str], artifact_name: str):
    matching = []

    print("ARTIFACTS", workflow_artifacts)

    for artifact in workflow_artifacts["artifacts"]:
        if artifact["name"] == artifact_name:
            matching.append(artifact)

    if len(matching) == 0:
        raise ArtifactNotFoundException()

    assert len(matching) == 1

    return matching[0]


def download_artifact(artifact_link: str, output_filepath: str):
    with requests.get(artifact_link, stream=True) as response:
        try:
            response.raise_for_status()
            with open(output_filepath, "wb") as f:
                for chunk in response.iter_content():
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        except requests.exceptions.HTTPError:
            print("RESPONSE", response.content)
            raise


def get_artifact_zip(
    runtime_url: str,
    owner: str,
    repo_name: str,
    run_id: str,
    token: str,
    artifact_name: str,
    output_filepath: str,
):

    for i in range(10):
        try:
            # First get artifact list
            artifact_list = list_artifacts(runtime_url, owner, repo_name, run_id, token)
            matching_artifact = filter_artifacts(artifact_list, artifact_name)
            print("MATCHING ARTIFACT", matching_artifact)
            download_artifact(
                matching_artifact["archive_download_url"], output_filepath
            )
            artifact_zip = ZipFile(output_filepath)
            return artifact_zip
        except ArtifactNotFoundException:
            time.sleep(1)
    else:
        raise ArtifactNotFoundException()


def main():
    token = os.environ["INPUT_REPO-TOKEN"]
    # github_api_url = os.environ["GITHUB_API_URL"]
    runtime_url = os.environ["ACTIONS_RUNTIME_URL"]
    run_id = int(os.environ["GITHUB_RUN_ID"])

    g = Github(token)
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    # workflow_run = repo.get_workflow_run(run_id)

    with tempfile.NamedTemporaryFile() as archive:
        artifact_zip = get_artifact_zip(
            runtime_url,
            repo.owner.login,
            repo.name,
            run_id,
            token,
            os.environ["INPUT_ARTIFACT-NAME"],
            archive.name,
        )
        print("ZIPFILE", artifact_zip.namelist())


if __name__ == "__main__":
    main()
