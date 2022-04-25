# Cloud Run Admin for Cloud Build
resource "google_project_iam_binding" "cloudbuild_run" {
  project = local.project
  role    = "roles/run.admin"

  members = [
    "serviceAccount:${local.project_number}@cloudbuild.gserviceaccount.com",
  ]
}

# Secret Accessor for Cloud Build
resource "google_project_iam_binding" "cloudbuild_secrets" {
  project = local.project
  role    = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${local.project_number}@cloudbuild.gserviceaccount.com",
  ]
}



# Secret Admin for Cloud Build
# <!-- Had to move this to manual boostrapping due to Cloud Build
#      Being used to run Terraform (TF in CB won't run properly 
#      unless it has Secret Manager Admin to manage secrets) --!> 
resource "google_project_iam_binding" "cloudbuild_secrets_admin" {
  project = local.project
  role    = "roles/secretmanager.admin"

  members = [
    "serviceAccount:${local.project_number}@cloudbuild.gserviceaccount.com",
  ]
}


# Service Account User for Cloud Build
resource "google_project_iam_binding" "cloudbuild_sa_user" {
  project = local.project
  role    = "roles/iam.serviceAccountUser"

  members = [
    "serviceAccount:${local.project_number}@cloudbuild.gserviceaccount.com",
  ]
}

# Worker Pool User for Cloud Build
resource "google_project_iam_binding" "cloudbuild_workerpools" {
  project = local.project
  role    = "roles/cloudbuild.workerPoolUser"

  members = [
    "serviceAccount:${local.project_number}@cloudbuild.gserviceaccount.com",
  ]
}
