#!/bin/bash

BUCKET_NAME=$DEVSHELL_PROJECT_ID
if [[ BUCKET_NAME ==  "" ]]

gsutil mb gs://$DEVSHELL_PROJECT_ID
