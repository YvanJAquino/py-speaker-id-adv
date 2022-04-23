#!/bin/bash

gsutil mb gs://$DEVSHELL_PROJECT_ID

gcloud iam service-accounts create svc-speaker-id \
    --description "Speaker ID service account" \
    --display-name "svc-speaker-id"

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:svc-speaker-id@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
    --role roles/cloudsql.editor

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:svc-speaker-id@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

# Org policies
# Domain restricted sharing: constraints/iam.allowedPolicyMemberDomains (required to release service)
# Trusted Image Projects: constraints/compute.trustedImageProjects 
#   projects/serverless-vpc-access-images (required for serverless VPC Access Connector)
# VM IP Forwarding: constraints/compute.vmCanIpForward

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member user:admin@yaquino.altostrat.com \
    --role roles/secretmanager.admin