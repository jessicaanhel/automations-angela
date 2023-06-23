#!/bin/bash

# Read repository mappings from a file
while IFS= read -r line || [[ -n "$line" ]]; do
    IFS='=' read -r -a mapping <<< "$line"
    BITBUCKET_REPO_URL="${mapping[0]}"
    GITHUB_REPO_URL="${mapping[1]}"

    # Extract the repository name from the Bitbucket URL
    REPO_NAME=$(basename "$BITBUCKET_REPO_URL" .git)

    # Clone the Bitbucket repository
    git clone "$BITBUCKET_REPO_URL"
    cd "$REPO_NAME"

    # Add GitHub as a remote
    git remote add github "$GITHUB_REPO_URL"

    for branch in $(git branch -r | grep -vE 'HEAD|master|origin/master'); do
        branch_name=$(echo "$branch" | sed 's/origin\///')
        git checkout -b "$branch_name" "origin/$branch_name"
        git push github "refs/remotes/origin/$branch_name:refs/heads/$branch_name"
        git checkout master
        git branch -D "$branch_name" 2>/dev/null
    done

    # Migrate authors
    git log --format='%aN <%aE>' | sort -fu > authors.txt
    git filter-repo --mailmap authors.txt


    # Push the rewritten history
    git branch -r | grep -v '\->' | while read -r remote_branch; do
        local_branch=$(echo "$remote_branch" | sed 's/origin\///')
        git push --force github "$local_branch":"$local_branch"
    done

    # Clean up
    rm authors.txt
    cd ..
    rm -rf "$REPO_NAME"

    echo "Repository migration completed for: $BITBUCKET_REPO_URL"
done < repo_mappings.txt

echo "All repository migrations completed successfully."
