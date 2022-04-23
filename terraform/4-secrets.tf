# Secret: Database Host
resource "google_secret_manager_secret" "secret_db_host" {
  secret_id = "DB_HOST"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version_secret_db_host" {
  secret = google_secret_manager_secret.secret_db_host.id
  secret_data = google_sql_database_instance.sql_speaker_id.private_ip_address
}

# Secret: Database Port
resource "google_secret_manager_secret" "secret_db_port" {
  secret_id = "DB_PORT"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version_secret_db_port" {
  secret = google_secret_manager_secret.secret_db_port.id
  secret_data = "5432"
}

# Secret: Database User
resource "google_secret_manager_secret" "secret_db_user" {
  secret_id = "DB_USER"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version_secret_db_user" {
  secret = google_secret_manager_secret.secret_db_user.id
  secret_data = local.db_user
}

# Secret: Database Password
resource "google_secret_manager_secret" "secret_db_pass" {
  secret_id = "DB_PASS"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version_secret_db_pass" {
  secret = google_secret_manager_secret.secret_db_pass.id
  secret_data = local.db_pass
}

# Secret: Database Name
resource "google_secret_manager_secret" "secret_db_name" {
  secret_id = "DB_NAME"
  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret_version" "version_secret_db_name" {
  secret = google_secret_manager_secret.secret_db_name.id
  secret_data = google_sql_database.db_speaker_id.name
}

# Secret: Database Connection String
resource "google_secret_manager_secret" "secret_db_cnst" {
  secret_id = "DB_CNST"
  replication {
    automatic = true
  }
}
# postgresql+psycopg2://USER:pass@HOST:PORT/NAME
resource "google_secret_manager_secret_version" "version_secret_db_cnst" {
  secret = google_secret_manager_secret.secret_db_cnst.id
  secret_data = "postgresql+psycopg2://${local.db_user}:${local.db_pass}@${google_sql_database_instance.sql_speaker_id.private_ip_address}:5432/${google_sql_database.db_speaker_id.name}"
}