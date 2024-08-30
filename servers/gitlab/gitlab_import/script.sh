#!/bin/bash
# requires curl and jq
# assumes usage of Gitlab API v4
# hella hacky
url="http://metis.lti.cs.cmu.edu:8023"
token=$GITLAB_TOKEN
username="$1"
# output is always paginated - get total number of pages from http header
numpages=$(curl -sSl -D - "$url/api/v4/users?order_by=id&per_page=50" --header "PRIVATE-TOKEN: $token" | grep -i 'x-total-pages' | awk -F ' ' '{print $2}') #| cut -c1 )
numpages="${numpages//$'\r'/}"
# iterate to all pages (each requires one API call)
for p in $(seq $numpages); do
# create temporary file to store json in and get data
    now=$(date +%Y%m%d_%H%M%S%z)-$p
    curl -s "$url/api/v4/users?per_page=50&page=$p" --header "PRIVATE-TOKEN: $token" >> $now-gitlab-users.json
# get number of entries on page using jq
    entries=$(cat $now-gitlab-users.json | jq '. | length')
# off by one, dirty as all heck. frick you
    entries=$(($entries-1))
# iterate through entries on page
for e in $(seq 0 $entries); do
if [[  $(cat $now-gitlab-users.json | jq .[$e].username | sed 's/\"//g') == "$username" ]]; then
# echo ID from json if username matches
            cat $now-gitlab-users.json | jq .[$e].id
            rm $now-gitlab-users.json
exit 0
fi
done
    rm $now-gitlab-users.json
done
exit 1
view raw