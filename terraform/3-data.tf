# Configure Cloud SQL 
resource "google_sql_database_instance" "sql_speaker_id" {
  provider         = google
  name             = "sql-speaker-id"
  database_version = "POSTGRES_14"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
  }
}

resource "google_sql_database" "db_speaker_id" {
  name     = "db_speaker_id"
  instance = google_sql_database_instance.sql_speaker_id.name
}

resource "google_sql_user" "admin" {
  name     = local.db_user
  instance = google_sql_database_instance.sql_speaker_id.name
  password = local.db_pass
}