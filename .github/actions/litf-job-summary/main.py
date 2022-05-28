# -*- coding: utf-8 -*-
import os

from github import Github


def main():
    g = Github(os.environ["INPUT_REPO-TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    workflow_run = repo.get_workflow_run(os.environ["GITHUB_RUN_ID"])
    print("RUN", workflow_run)


if __name__ == "__main__":
    main()
