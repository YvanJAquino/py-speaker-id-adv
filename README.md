# py-speaker-id-adv

# Instructions
## Bootstrapping

## Build the Terraform Cloud Builder
The resulting builder's name is is gcr.io/${PROJECT_ID}/terraform

```shell
git clone https://github.com/GoogleCloudPlatform/cloud-builders-community.git
cd cloud-builders-community/terraform/
gcloud builds submit \
    --substitutions _TERRAFORM_VERSION=1.1.8,_TERRAFORM_VERSION_SHA256SUM=fbd37c1ec3d163f493075aa0fa85147e7e3f88dd98760ee7af7499783454f4c5
```

## 
