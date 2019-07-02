terraform {
  backend "remote" {
    hostname = "tfe-poc.apac.squadzero.io"
    organization = "contino"

    workspaces {
      name = "test-project"
    }
  }
}

provider "null" {
  version = "2.1.2"
}

module "test-module" {
  source = "./test-module"
  network_name = "${var.network_name}"
  gcp_project_id = "${var.gcp_project_id}"
  vault_address = "${var.vault_address}"
  vault_secret_path = "${var.vault_secret_path}"
}


