provider "google" {
  project = "${var.gcp_project_id}"
  version = "2.9.1"
  access_token = data.vault_generic_secret.gcp_token.data["token"]
  region = "australia-southeast1"
}

provider "vault" {
  address = "${var.vault_address}"
  version = "2.0.0"
}

data "vault_generic_secret" "gcp_token" {
  path = "${var.vault_secret_path}"
}

resource "google_compute_network" "vpc_network" {
  name                    = "${var.network_name}"
  auto_create_subnetworks = "true"
}

resource "google_compute_firewall" "ssh-only" {
  name    = "test-firewall"
  network = "${google_compute_network.vpc_network.self_link}"

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}

resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "f1-micro"
  zone         = "australia-southeast1-b"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "${google_compute_network.vpc_network.self_link}"
    access_config {
      nat_ip = "${google_compute_address.static.address}"
    }
  }

}
