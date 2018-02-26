#!/bin/bash

#
# Usage: slackpost <channel> <message>
#

channel=$1

if [[ $channel == "" ]]
then
        echo "No channel specified"
        exit 1
fi

shift

text=$*

if [[ $text == "" ]]
then
        echo "No text specified"
        exit 1
fi

escapedText=$(echo $text | sed 's/"/\"/g' | sed "s/'/\'/g" )
json="{\"channel\": \"#$channel\", \"text\": \"$escapedText\"}"

curl -s -d "payload=$json" "https://hooks.slack.com/services/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"
