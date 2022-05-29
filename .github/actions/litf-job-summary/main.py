# -*- coding: utf-8 -*-
import os
import tempfile
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


def filter_artifacts(workflow_artifacts: dict[str, str], artifact_name: str):
    matching = []

    print("ARTIFACTS", workflow_artifacts["artifacts"])

    for artifact in workflow_artifacts["artifacts"]:
        if artifact["name"] == artifact_name:
            matching.append(artifact)

    print("MATCHING", matching)

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


def main():
    token = os.environ["INPUT_REPO-TOKEN"]
    github_api_url = os.environ["GITHUB_API_URL"]
    run_id = int(os.environ["GITHUB_RUN_ID"])

    g = Github(token)
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    # workflow_run = repo.get_workflow_run(run_id)

    # First get artifact list
    artifact_list = list_artifacts(
        github_api_url, repo.owner.login, repo.name, run_id, token
    )
    matching_artifact = filter_artifacts(
        artifact_list, os.environ["INPUT_ARTIFACT-NAME"]
    )
    print("MATCHING ARTIFACT", matching_artifact)
    with tempfile.NamedTemporaryFile() as archive:
        download_artifact(matching_artifact["archive_download_url"], archive.name)
        artifact_zip = ZipFile(archive.name)
        print("ZIPFILE", artifact_zip.namelist())


if __name__ == "__main__":
    main()
