# Construct the network
resource "google_compute_network" "vpc" {
    provider                = google
    name                    = "vpc-${var.name}"
    auto_create_subnetworks = false
}

# Construct the data subnet (with a secondary / alias ip range)
resource "google_compute_subnetwork" "default" {
    provider                   = google
    network                    = google_compute_network.vpc.id
    name                       = "subnet-default-${var.name}"
    ip_cidr_range              = "10.0.0.0/24"
    private_ip_google_access   = true
    private_ipv6_google_access = true
}

# Configure Cloud NAT
resource "google_compute_router" "nat_router" {
  provider = google
  name     = "router-${var.name}"
  network = google_compute_network.vpc.id
}
resource "google_compute_router_nat" "nat" {
  provider                           = google
  name                               = "nat-${var.name}"
  router                             = google_compute_router.nat_router.name
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

# Configure Serverless VPC access connector
resource "google_vpc_access_connector" "connector" {
  name          = "serverless-vpc-access"
  provider      = google
  ip_cidr_range = "10.255.255.240/28"
  network       = google_compute_network.default.name
}

# Allow traffic from ICMP
resource "google_compute_firewall" "icmp_ingress" {
    provider = google
    name = "fw-${google_compute_network.vpc.name}-allow-icmp"
    network = google_compute_network.vpc.id
    direction = "INGRESS"
    source_ranges = ["0.0.0.0/0"]
    allow {
        protocol = "icmp"
    }
}
# Allow traffic from TCP (TCP 22)
resource "google_compute_firewall" "ssh_ingress" {
    provider = google
    name = "fw-${google_compute_network.vpc.name}-allow-ssh"
    network = google_compute_network.vpc.id
    direction = "INGRESS"
    source_ranges = ["0.0.0.0/0"]
    allow {
        protocol = "tcp"
        ports = ["22"]
    }
}
# Allow traffic from RDP (TCP 3389)
resource "google_compute_firewall" "rdp_ingress" {
    provider = google
    name = "fw-${google_compute_network.vpc.name}-allow-rdp"
    network = google_compute_network.vpc.id
    direction = "INGRESS"
    source_ranges = ["0.0.0.0/0"]
    allow {
        protocol = "tcp"
        ports = ["3389"]
    }
}

# Allow traffic from IAP (TCP 22 , 3389).
resource "google_compute_firewall" "iap_ingress" {
    provider = google
    name = "fw-${google_compute_network.vpc.name}-allow-iap"
    network = google_compute_network.vpc.id
    direction = "INGRESS"
    source_ranges = ["35.235.240.0/20"]

    allow {
        protocol = "tcp"
        ports = [
            "22",
            "3389"
        ]
    }
}
