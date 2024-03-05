PR_URL="https://stash.jamf.build/projects/DOC/repos/mysql/pull-requests/131/overview"

for branch in $(git branch); do
    echo $branch;
    git checkout $branch;
    git pull $PR_URL $branch --strategy=recursive -X theirs;
done