# -*- coding: utf-8 -*-
import os

import requests
from github import Github


def list_artifacts(github_api_url: str, owner: str, repo: str, run_id: str, token: str):
    list_artifacts_url = (
        f"{github_api_url}/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    )
    headers = {
        "Authorization": f"token {token}",
    }

    response = requests.get(list_artifacts_url, headers=headers)
    response.raise_for_status()

    return response.json()


def download_artifact():
    pass


def main():
    token = os.environ["INPUT_REPO-TOKEN"]
    github_api_url = os.environ["GITHUB_API_URL"]
    run_id = int(os.environ["GITHUB_RUN_ID"])

    g = Github(token)
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    # workflow_run = repo.get_workflow_run(run_id)

    # First get artifact list
    artifact_list = list_artifacts(github_api_url, repo.owner, repo.name, run_id, token)
    print("ARTIFACT LIST", artifact_list)

    # TODO: Download the artifact automatically

    output_dir = os.environ["INPUT_INPUT-PATH"]
    print("LS", os.listdir("/tmp"))
    print("LS", os.listdir(output_dir))


if __name__ == "__main__":
    main()
