from kubernetes import client, config
import kubernetes_helper
import storage_account_helper
import json
import collections


def get_json_configurations(json_file):
    """
    Get parsed configurations json file
    """
    with open(json_file, 'r') as config_file:
        parsed_dict = json.load(
            config_file, object_pairs_hook=collections.OrderedDict)

    return parsed_dict


def main():

    # Set configurations
    configuration_file = "configuration.json"
    parsed_data = get_json_configurations(configuration_file)
    queues = parsed_data["queues"]
    user = parsed_data["user"]
    cluster = parsed_data["cluster"]["name"]
    cluster_rg = parsed_data["cluster"]["resource_group"]
    kube_pass = " "  # The AKS cred pass

    storage_account = ""
    queue_client = None

    # Set Kubernetes Client
    kubernetes_helper.login_to_aks(user, cluster, cluster_rg, kube_pass)
    config.load_kube_config()
    app_client = client.AppsV1Api()

    # Listen to queues
    while True:
        for queue in queues:
            queue_name = queue["queue_name"]
            if storage_account != queue["storage_account"]:
                storage_account = queue["storage_account"]
                queue_client = storage_account_helper.get_storage_account_queue_client(
                    storage_account, queue["primary_key"], queue_name)
            print(f"Getting {queue_name} messages length...")
            msg_length = storage_account_helper.get_queue_length(queue_client)
            if msg_length != None:
                replica = msg_length*2
                kubernetes_helper.update_deployments_scale(
                    queue["deployments"], replica, app_client)


if __name__ == "__main__":
    main()
