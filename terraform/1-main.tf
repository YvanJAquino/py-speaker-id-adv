# Google Cloud Provider
provider "google"  {
    alias = "default"
}

# Attributes include: access_token, project, region, and zone
data "google_client_config" "default" {
    provider = google.default
}

# Attributes: keepers, id, and result (id == result)
resource "random_uuid" "db_pass" {
}

# Redefining variables
locals {
    project = coalesce(var.project_id, data.google_client_config.default.project)
    region  = coalesce(var.region, data.google_client_config.default.region)
    db_pass = coalesce(var.db_pass, random_uuid.db_pass.id)
    db_user = var.db_user
}

# Recreate the provider based on defaults or user-provided variables.
provider "google" {
    project = local.project
    region  = local.region
}

data "google_project" "project" {
}

locals {
    project_number = coalesce(var.project_number, data.google_project.project.number)
}

# If applying this directly, the bucket must exist first.
terraform {
  backend "gcs" {
    bucket = "oceanic-muse-348113"
    prefix = "terraform"
  }
}

# Enable the Cloud Resource Manager API
resource "google_project_service" "resource_manager" {
    provider = google
    service  = "cloudresourcemanager.googleapis.com"
    disable_on_destroy = false
}


# Enable the Storage API
resource "google_project_service" "storage" {
    provider = google
    service  = "storage.googleapis.com"
    disable_on_destroy = false
}

# Enable the IAM API
resource "google_project_service" "iam" {
    provider = google
    service  = "iam.googleapis.com"
    disable_on_destroy = false
}

# Enable the Compute API
resource "google_project_service" "compute" {
    provider = google
    service  = "compute.googleapis.com"
    disable_on_destroy = false
}

# Enable the IAP API
resource "google_project_service" "iap" {
    provider = google
    service  = "iap.googleapis.com"
    disable_on_destroy = false
}

# Enable the Cloud Run API
resource "google_project_service" "run" {
    provider = google
    service  = "run.googleapis.com"
    disable_on_destroy = false
}

# Enable the SQL Admin API
resource "google_project_service" "sqladmin" {
    provider = google
    service  = "sqladmin.googleapis.com"
    disable_on_destroy = false
}

# Enable the SQL Component API
resource "google_project_service" "sql_component" {
    provider = google
    service  = "sql-component.googleapis.com"
    disable_on_destroy = false
}

# Enable the Secret Manager API
resource "google_project_service" "secretmanager" {
    provider = google
    service  = "secretmanager.googleapis.com"
    disable_on_destroy = false
}

# Enable the Cloud Build API
resource "google_project_service" "cloudbuild" {
    provider = google
    service  = "cloudbuild.googleapis.com"
    disable_on_destroy = false
}

# Enable the Serverless VPC Access API
# Sometimes this doesn't get turned on - no idea why.
resource "google_project_service" "vpcaccess" {
    provider = google
    service  = "vpcaccess.googleapis.com"
    disable_on_destroy = false
}

#Enable the Service Networking API (private SQL Connections)
# Sometimes this doesn't get turned on - no idea why.
resource "google_project_service" "service_networking" {
    provider = google
    service  = "servicenetworking.googleapis.com"
    disable_on_destroy = false
}


# # Not working; says I can't use my identity with orgpolicy.googleapis.com
# resource "google_org_policy_policy" "trusted_images" {
#     name   = "projects/${local.project}/policies/compute.trustedImageProjects"
#     parent = "projects/${local.project}"
#     spec {
#         rules {
#             values {
#                 allowed_values = [
#                     "projects/deeplearning-platform-release"
#                 ]
#             }
#         }
#     }
# }