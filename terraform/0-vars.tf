variable "name" {
    type = string
    default = "df-cx-speaker-id"
}

variable "project_id" {
    type = string
    # Use the google_client_config    
    default = null
}

variable "region" {
    type = string
    default = "us-central1"
}

variable "db_user" {
    type = string
    default = "svc-speaker-id"
}

variable "db_pass" {
    type = string
    # Create a UUID unless this is specified.
    default = null
}