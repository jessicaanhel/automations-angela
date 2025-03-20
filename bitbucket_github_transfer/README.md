# Bitbucket to GitHub Repository Migration

This script automates the process of migrating repositories from Bitbucket to GitHub, including branches, commits, and authors.

## Setup

1Modify the `REPO_MAPPINGS` array in the script to specify the repository mappings. Each entry should follow the format `BITBUCKET_REPO_URL=GITHUB_REPO_URL`, where `BITBUCKET_REPO_URL` is the Bitbucket repository URL and `GITHUB_REPO_URL` is the GitHub repository URL.

2Run the script:
   bash migration.sh

## Notes

- The script assumes that you have appropriate access to both the Bitbucket and GitHub repositories.

- The script clones the Bitbucket repository, adds the GitHub repository as a remote, pushes branches to GitHub, and cleans up the local repository.

- If you encounter any issues or errors during the migration process, please review the script and ensure that the repository URLs and mappings are correct.

- This script does not migrate issues, pull requests, or other metadata. It focuses on transferring the codebase and branch history.
