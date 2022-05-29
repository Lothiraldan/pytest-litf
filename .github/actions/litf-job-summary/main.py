# -*- coding: utf-8 -*-
import os
import tempfile
import time
from typing import Dict
from zipfile import ZipFile

import requests
from github import Github


def list_artifacts(
    github_api_url: str, owner: str, repo: str, run_id: str, token: str
) -> dict[str, str]:
    list_artifacts_url = (
        f"{github_api_url}/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    )
    headers = {
        "Authorization": f"token {token}",
    }

    with requests.get(list_artifacts_url, headers=headers) as response:
        response.raise_for_status()

        return response.json()


class ArtifactNotFoundException(Exception):
    pass


def filter_artifacts(workflow_artifacts: Dict[str, str], artifact_name: str):
    matching = []

    print("ARTIFACTS", workflow_artifacts["artifacts"])

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
    github_api_url: str,
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
            artifact_list = list_artifacts(
                github_api_url, owner, repo_name, run_id, token
            )
            matching_artifact = filter_artifacts(artifact_list, artifact_name)
            print("MATCHING ARTIFACT", matching_artifact)
            download_artifact(
                matching_artifact["archive_download_url"], output_filepath
            )
            artifact_zip = ZipFile(output_filepath)
            return artifact_zip
        except ArtifactNotFoundException:
            time.sleep(1)


def main():
    token = os.environ["INPUT_REPO-TOKEN"]
    github_api_url = os.environ["GITHUB_API_URL"]
    run_id = int(os.environ["GITHUB_RUN_ID"])

    g = Github(token)
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    # workflow_run = repo.get_workflow_run(run_id)

    with tempfile.NamedTemporaryFile() as archive:
        artifact_zip = get_artifact_zip(
            github_api_url,
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
