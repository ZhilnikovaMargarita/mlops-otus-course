yc_config = {
  token     = ""
  cloud_id  = ""
  folder_id = ""
  zone      = "ru-central1-a"
}
yc_instance_user        = "ubuntu"
yc_instance_name        = "airflow-cluster"
yc_network_name         = "airflow-network"
yc_subnet_name          = "airflow-subnet"
yc_service_account_name = "airflow-cluster-sa"
yc_bucket_name          = "airflow-bucket"
yc_storage_endpoint_url = "https://storage.yandexcloud.net"
admin_password          = "Admin-007"
public_key_path         = "/Users/rita/.ssh/id_rsa.pub"  # public ssh key path.pub
private_key_path        = "/Users/rita/.ssh/id_rsa"  # private ssh key path
