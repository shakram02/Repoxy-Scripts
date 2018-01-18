#!/usr/bin/env bash

update(){
    RED='\033[33;31m'
	YELLOW='\033[33;33m'
	GREEN='\033[33;32m'
	NC='\033[0m' # No Color

	if ! [ -d .git ]; then
		echo "${RED}This is not a git repo${NC}"
		return 1
	fi

	HEAD=$(git rev-parse HEAD)
	CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD)

	echo "Fetching..."
	git fetch --all --prune &>/dev/null
	if [ $? -ne 0 ]; then
		echo "${RED}Fetch Failed!${NC}"
		return 1
	fi

    for branch in `git for-each-ref --format='%(refname:short)' refs/heads`; do
	    echo "${YELLOW}Updading origin/${branch}...${NC}"
	    $(git checkout ${branch})
	    $(git rebase origin/${branch})
	done

    echo "${YELLOW}Returning to working branch...{$NC}"
	$(git checkout ${CUR_BRANCH})
}

update
