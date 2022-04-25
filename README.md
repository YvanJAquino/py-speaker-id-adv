# py-speaker-id-adv

# Instructions
Terraform is EXPERIMENTAL!  
## Bootstrapping
### A New Project
Make a new project.  Re-initialize gcloud to use the new project.
```shell
gcloud init
```
Clone the Speaker Id Repo
```shell
git clone https://github.com/YvanJAquino/py-speaker-id-adv
```

### Terraform State Backend
Make a new project and create a new bucket with the name of the project
```shell
gsutil mb gs://$DEVSHELL_PROJECT_ID
```

Update the terraform backend block in 1-main.tf MANUALLY.  The terraform backend block appears around L37.
```terraform
terraform {
  backend "gcs" {
    bucket = "REPLACE_WITH_PROJECT_ID_MANUALLY"
    prefix = "terraform"
  }
}
```

### Update Cloudbuild Service Account with IAM Roles
Add the following roles to Cloud Build's service account.  The Cloud Build service acccount has the following format:
```
[projectNumber]@cloudbuild.gserviceaccount.com
```
Use gcloud to generate the e-mail.

```
export CB_SA=$(gcloud projects describe $DEVSHELL_PROJECT_ID --format="value(projectNumber)")@cloudbuild.gserviceaccount.com

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:$CB_SA \
    --role roles/run.admin

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:$CB_SA \
    --role roles/secretmanager.admin

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:$CB_SA \
    --role roles/iam.serviceAccountUser

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:$CB_SA \
    --role roles/cloudbuild.workerPoolUser
```

### Organization Policies
Check the following organization policies:

```shell
- constraints/compute.vmCanIpForward (required for Serverless VPC Access Connector)

- constraints/iam.allowedPolicyMemberDomains (required for Cloud Run)

- constraints/compute.restrictVpcPeering (required for Cloud SQL)

- constraints/compute.trustedImageProjects (Required for S-VPC-A: projects/serverless-vpc-access-images
)
```

### IAM
```shell
- roles/secretmanager.admin (Cloud Build Svc Acct)

- roles/run.admin (Cloud Build Svc Acct)

- roles/cloudsql.admin (Cloud Build Svc Acct)
```

### Required Services and APIs
```shell
- cloudresourcemanager.googleapis.com (Required for Terraform in Cloud Build: CRUD for GCP resource containers)
```


## Build the Terraform Cloud Builder
The resulting builder's name is is gcr.io/${PROJECT_ID}/terraform

```shell
git clone https://github.com/GoogleCloudPlatform/cloud-builders-community.git
cd cloud-builders-community/terraform/
gcloud builds submit \
    --substitutions _TERRAFORM_VERSION=1.1.8,_TERRAFORM_VERSION_SHA256SUM=fbd37c1ec3d163f493075aa0fa85147e7e3f88dd98760ee7af7499783454f4c5
```

## 
