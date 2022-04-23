resource "google_secret_manager_secret" "secret-db-host" {
  secret_id = "DB_HOST"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version-secret-db-host" {
  secret = google_secret_manager_secret.secret-db-host.id
  secret_data = "FILL_ME_IN"
}

resource "google_secret_manager_secret" "secret-db-port" {
  secret_id = "DB_PORT"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version-secret-db-port" {
  secret = google_secret_manager_secret.secret-db-port.id
  secret_data = "FILL_ME_IN"
}

resource "google_secret_manager_secret" "secret-db-user" {
  secret_id = "DB_USER"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version-secret-db-user" {
  secret = google_secret_manager_secret.secret-db-user.id
  secret_data = "FILL_ME_IN"
}

resource "google_secret_manager_secret" "secret-db-pass" {
  secret_id = "DB_PASS"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version-secret-db-pass" {
  secret = google_secret_manager_secret.secret-db-pass.id
  secret_data = "FILL_ME_IN"

resource "google_secret_manager_secret" "secret-db-name" {
  secret_id = "DB_NAME"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version-secret-db-name" {
  secret = google_secret_manager_secret.secret-db-name.id
  secret_data = "FILL_ME_IN"
}