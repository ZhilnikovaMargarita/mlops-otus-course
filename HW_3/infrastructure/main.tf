# IAM ресурсы
resource "yandex_iam_service_account" "sa" {
  name        = var.yc_service_account_name
  description = "Service account for Dataproc cluster and related services"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_roles" {
  for_each = toset([
    "storage.admin",
    "dataproc.editor",
    "compute.admin",
    "dataproc.agent",
    "mdb.dataproc.agent",
    "vpc.user",
    "iam.serviceAccounts.user",
    "storage.uploader",
    "storage.viewer",
    "storage.editor"
  ])

  folder_id = var.yc_folder_id
  role      = each.key
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa.id
  description        = "Static access key for object storage"
}

# Network ресурсы
resource "yandex_vpc_network" "network" { // сеть
  name = var.yc_network_name
}

resource "yandex_vpc_subnet" "subnet" { // подсеть
  name           = var.yc_subnet_name
  zone           = var.yc_zone
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = [var.yc_subnet_range]
  route_table_id = yandex_vpc_route_table.route_table.id
}

resource "yandex_vpc_gateway" "nat_gateway" { // шлюз
  name = var.yc_nat_gateway_name
  shared_egress_gateway {}
}

resource "yandex_vpc_route_table" "route_table" { // таблица маршрутизации
  name       = var.yc_route_table_name
  network_id = yandex_vpc_network.network.id

  static_route {
    destination_prefix = "0.0.0.0/0"
    gateway_id         = yandex_vpc_gateway.nat_gateway.id
  }
}

resource "yandex_vpc_security_group" "security_group" { // группа безопасности
  name        = var.yc_security_group_name
  description = "Security group for Dataproc cluster"
  network_id  = yandex_vpc_network.network.id

  ingress {
    protocol       = "ANY"
    description    = "Allow all incoming traffic"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol       = "TCP"
    description    = "UI"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 443
  }

  ingress {
    protocol       = "TCP"
    description    = "SSH"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 22
  }

  ingress {
    protocol       = "TCP"
    description    = "Jupyter"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 8888
  }

  egress {
    protocol       = "ANY"
    description    = "Allow all outgoing traffic"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol       = "ANY"
    description    = "Allow all outgoing traffic"
    from_port      = 0
    to_port        = 65535
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol          = "ANY"
    description       = "Internal"
    from_port         = 0
    to_port           = 65535
    predefined_target = "self_security_group"
  }
}

# Dataproc ресурсы
resource "yandex_dataproc_cluster" "dataproc_cluster" {
  depends_on  = [yandex_resourcemanager_folder_iam_member.sa_roles]
  # bucket      = yandex_storage_bucket.data_bucket.bucket
  bucket      = var.yc_bucket_name  # возьмем созанный ранее бакет
  description = "Dataproc Cluster created by Terraform for OTUS project"
  name        = var.yc_dataproc_cluster_name
  labels = {
    created_by = "terraform"
  }
  service_account_id = yandex_iam_service_account.sa.id
  zone_id            = var.yc_zone
  security_group_ids = [yandex_vpc_security_group.security_group.id]


  cluster_config {
    version_id = var.yc_dataproc_version

    hadoop {
      services = ["HDFS", "YARN", "SPARK"]
      properties = {
        "yarn:yarn.resourcemanager.am.max-attempts" = 5
      }
      ssh_public_keys = [file(var.public_key_path)]
    }

    subcluster_spec {
      name = "master"
      role = "MASTERNODE"
      resources {
        resource_preset_id = var.dataproc_master_resources.resource_preset_id
        disk_type_id       = "network-ssd"
        disk_size          = var.dataproc_master_resources.disk_size
      }
      subnet_id        = yandex_vpc_subnet.subnet.id
      hosts_count      = 1
      assign_public_ip = true
    }

    subcluster_spec {
      name = "data"
      role = "DATANODE"
      resources {
        resource_preset_id = var.dataproc_data_resources.resource_preset_id
        disk_type_id       = "network-ssd"
        disk_size          = var.dataproc_data_resources.disk_size
      }
      subnet_id   = yandex_vpc_subnet.subnet.id
      hosts_count = 1
    }

    subcluster_spec {
      name = "compute"
      role = "COMPUTENODE"
      resources {
        resource_preset_id = var.dataproc_compute_resources.resource_preset_id
        disk_type_id       = "network-ssd"
        disk_size          = var.dataproc_compute_resources.disk_size
      }
      subnet_id   = yandex_vpc_subnet.subnet.id
      # hosts_count = 3
      hosts_count = 1
    }
  }
}

# Compute ресурсы
resource "yandex_compute_disk" "boot_disk" {
  name     = "boot-disk"
  zone     = var.yc_zone
  image_id = var.yc_image_id
  size     = 30
}

resource "yandex_compute_instance" "proxy" {
  name                      = var.yc_instance_name
  allow_stopping_for_update = true
  platform_id               = "standard-v3"
  zone                      = var.yc_zone
  service_account_id        = yandex_iam_service_account.sa.id

  metadata = {
    ssh-keys = "ubuntu:${file(var.public_key_path)}"
    user-data = <<-EOF
      #!/bin/bash
      mkdir -p /home/ubuntu/.ssh
      echo "${file(var.private_key_path)}" > /home/ubuntu/.ssh/dataproc
      chmod 600 /home/ubuntu/.ssh/dataproc
      chown ubuntu:ubuntu /home/ubuntu/.ssh/dataproc
      eval `ssh-agent -s`
      ssh-add /home/ubuntu/.ssh/dataproc
    EOF
  }

  scheduling_policy {
    preemptible = true // создаем прерываемую виртуальную машину (для экономии средств)
  }

  resources {
    cores  = 2
    memory = 16
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot_disk.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata_options {
    gce_http_endpoint = 1
    gce_http_token    = 1
  }

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file(var.private_key_path)
    host        = self.network_interface[0].nat_ip_address
  }

  provisioner "remote-exec" {
    inline = [
      "sudo cloud-init status --wait",
      "echo 'User-data script execution log:' | sudo tee /var/log/user_data_execution.log",
      "sudo cat /var/log/cloud-init-output.log | sudo tee -a /var/log/user_data_execution.log",
    ]
  }
  depends_on = [yandex_dataproc_cluster.dataproc_cluster]
}
