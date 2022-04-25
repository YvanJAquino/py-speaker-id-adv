# py-speaker-id-adv

# Instructions
## Bootstrapping
### Terraform State Backend
Make a new project and create a new buckcet with the name of the project
```shell
gsutil mb gs://$DEVSHELL_PROJECT_ID
```

### Organization Policies
Check the following organization policies:

```shell
- constraints/compute.vmCanIpForward (required for Serverless VPC Access Connector)

- constraints/iam.allowedPolicyMemberDomains (required for Cloud Run)

- constraints/compute.restrictVpcPeering (required for Cloud SQL)

- constraints/compute.trustedImageProjects (Required for S-VPC-A)
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
