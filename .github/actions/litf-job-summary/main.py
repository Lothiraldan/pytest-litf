# -*- coding: utf-8 -*-
import os

from github import Github


def main():
    g = Github(os.environ["INPUT_REPO-TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    workflow_run = repo.get_workflow_run(int(os.environ["GITHUB_RUN_ID"]))
    print("RUN", workflow_run)

    # TODO: Download the artifact automatically

    output_dir = os.environ["INPUT_INPUT-PATH"]
    print("LS", os.listdir("/tmp"))
    print("LS", os.listdir(output_dir))


if __name__ == "__main__":
    main()
