#!/bin/bash

set -euo pipefail

# Constants
COMMIT_STATIC_PERMIT_LIST="(^Merge pull request \#)|(^Merge( remote-tracking)? branch)|(^Add .whitesource configuration file)|(^Revert \""

# Find current branch or tag name
get_current_branch_name() {
  local current_ref=$(git symbolic-ref -q HEAD || git describe --tags --exact-match)
  echo "Current ref: $current_ref"

  if [[ "$current_ref" =~ ^refs/heads/ ]]; then
    echo "${current_ref#refs/heads/}"
  elif [[ "$current_ref" =~ ^refs/tags/ ]]; then
    echo "${current_ref#refs/tags/}"
  elif [[ "$current_ref" =~ ^[0-9] ]]; then
    echo "$current_ref"
  else
    echo "❌ Unknown ref format: $current_ref" >&2
    exit 1
  fi
}

# Log colors
log_info()    { echo -e "\033[34m[INFO]\033[0m $*"; }
log_success() { echo -e "\033[32m[SUCCESS]\033[0m $*"; }
log_warn()    { echo -e "\033[33m[WARNING]\033[0m $*"; }
log_error()   { echo -e "\033[31m[ERROR]\033[0m $*"; }

is_static_permitted() {
  echo "$1" | grep -qiE "$COMMIT_STATIC_PERMIT_LIST"
}

has_valid_prefix() {
  local commit_message="$1"
  shift
  local prefixes=("$@")
  for prefix in "${prefixes[@]}"; do
    if echo "$commit_message" | grep -qiE "^($prefix)"; then
      return 0
    fi
  done
  return 1
}

starts_with_fixup_and_amend() {
  local commit_message="$1"
  if echo "$commit_message" | grep -qiE '^(fixup)!'; then
    echo "❌ !fixup commit is not allowed: \"$commit_message\""
    return 0
  elif echo "$commit_message" | grep -qiE '^(amend)!'; then
    echo "❌ amend! commit is not allowed: \"$commit_message\""
    return 0
  fi
  return 1
}

validate_inclusions() {
  local commit_message="$1"

  if is_static_permitted "$commit_message"; then
    echo "✔ Commit matches static permit-list: \"$commit_message\""
    return 0
  fi

  if has_valid_prefix "$commit_message" "${PREFIXES[@]}"; then
    echo "✔ Commit matches allowed prefix: \"$commit_message\""
    return 0
  fi
}

validate_exclusions() {
  local commit_message="$1"

  if starts_with_fixup_and_amend "$commit_message"; then
    invalid_commits+=("!fixup and amend! commit is not allowed: $commit_message")
    return 0
  fi
}

extract_ticket() {
  echo "$1" | grep -oEi '[a-zA-Z]+-[0-9]+' | head -n 1 || true
}

check_jira_ticket_api() {
  local ticket="$1"
  local jira_url="$2"
  local username="$3"
  local api_token="$4"

  response=$(curl -s --url "${jira_url}/rest/api/3/issue/${ticket}" \
    --header 'Accept: application/json' \
    --user "${username}:${api_token}" 2>&1)

  if echo "$response" | grep -q '"errorMessages"'; then
    return 1
  else
    return 0
  fi
}

check_existens_of_ticket_in_jira() {
  local commit_message="$1"
  local jira_url="$2"
  local jira_username="$3"
  local jira_api_token="$4"

  TICKET_TO_CHECK=$(extract_ticket "$commit_message")

  if [ -z "$TICKET_TO_CHECK" ]; then
    echo "❌ Invalid commit message: \"$commit_message\". Jira ticket is empty."
    invalid_commits+=("Invalid commit message: $commit_message")
    return 0
  fi

  if ! check_jira_ticket_api "$TICKET_TO_CHECK" "$jira_url" "$jira_username" "$jira_api_token"; then
    echo "⚠️ Ticket $TICKET_TO_CHECK in commit \"$commit_message\" does not exist in \"$jira_url\"."
    warnings+=("Jira ticket does not exist: $commit_message in $jira_url.")
  else
    echo "✔ Ticket $TICKET_TO_CHECK in commit \"$commit_message\" is valid."
  fi
}

validate_commits() {
  local jira_username="$1"
  local jira_api_token="$2"
  local jira_url="$3"
  local allowed_prefixes="$4"
  local branch_merge_base="$5"

  invalid_commits=()
  warnings=()

  IFS=',' read -r -a PREFIXES <<< "$allowed_prefixes"

  BRANCH_COMMITS=$(git rev-list "${branch_merge_base}..HEAD")

  while IFS= read -r commit; do
    commit_message=$(git log --max-count=1 --format=%B "$commit")

    validate_inclusions "$commit_message"
    validate_exclusions "$commit_message"
    check_existens_of_ticket_in_jira "$commit_message" "$jira_url" "$jira_username" "$jira_api_token"

  done <<< "$BRANCH_COMMITS"

  if [ ${#invalid_commits[@]} -gt 0 ]; then
    echo ""
    log_error "🚨🚨🚨  Your PR was rejected because at least one commit message on this branch is invalid 🚨🚨🚨"
    log_error "Build failed due to the following issues:"
    for commit in "${invalid_commits[@]}"; do
      log_error "❌ $commit"
    done

    if [ ${#warnings[@]} -gt 0 ]; then
      log_warn "🔔 Warnings to fix:"
      for warning in "${warnings[@]}"; do
        log_warn "$warning"
      done
    fi

    log_error "Please fix the commit message(s)"
    log_error "If there is a failure, users should rebase their branch's commit history to contain only valid commits that link real Jira tickets."

    exit 1

  elif [ ${#warnings[@]} -gt 0 ]; then
    log_warn "Build failed due to warnings:"
    for warning in "${warnings[@]}"; do
      log_warn "$warning"
    done
    exit 1

  else
    log_success "All commits are valid."
  fi
}

validate_commits_in_pr() {
  local jira_username="$1"
  local jira_api_token="$2"
  local jira_url="$3"
  local allowed_prefixes="$4"

  CURRENT_BRANCH=$(get_current_branch_name)

  if git show-ref --verify --quiet "refs/heads/$CURRENT_BRANCH"; then
    BRANCH_MERGE_BASE=$(git merge-base origin/main "$CURRENT_BRANCH")
  else
    BRANCH_MERGE_BASE=$(git rev-list -n 1 "$CURRENT_BRANCH")
  fi

  validate_commits "$jira_username" "$jira_api_token" "$jira_url" "$allowed_prefixes" "$BRANCH_MERGE_BASE"
}

validate_last_commit () {
  local jira_username="$1"
  local jira_api_token="$2"
  local jira_url="$3"
  local allowed_prefixes="$4"

  CURRENT_BRANCH=$(get_current_branch_name)
  BRANCH_MERGE_BASE=$(git rev-parse "$CURRENT_BRANCH~1")

  validate_commits "$jira_username" "$jira_api_token" "$jira_url" "$allowed_prefixes" "$BRANCH_MERGE_BASE"
}