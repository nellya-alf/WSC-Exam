from kubernetes import client, config
from az.cli import az


def login_to_aks(user, cluster, resource_group, password):
    """
    Login to Azure account, and gets the aks credentials

    Parameters
    ----------
    user: Azure user
    cluster: AKS cluster name
    resource_group: AKS resource group
    password: Azure user pass
    """
    az_args = f"login -u {user} -p {password}"
    az(az_args)
    aks_args = f"aks get-credentials --name {cluster} --resource-group {resource_group}"
    az(aks_args)


def get_current_deployment_scale(name, namespace, client):
    """
    Get a deployment scale replica

    Parameters
    ----------
    name: the name of the deployment
    namespace: the namespace of the deployment
    client: kubernetes client 

    Returns
    ------- 
        The number of the messages in queue
    """
    try:
        responce = client.read_namespaced_deployment_scale(name, namespace)
    except Exception as err:
        raise f"Failed to get {name} deployment scale, an error accrued:{err}"
    return responce.status.replicas


def update_deployments_scale(deployments, replica_count, client):
    """
    Update the replica number of a deployment

    Parameters
    ----------
    deployments: list of deployments objects
    replica_count: the number of the replicas
    client: kubernetes client
    """
    for deployment in deployments:
        deployment_name = deployment["name"]
        namespace = deployment["namespace"]
        body = {'spec': {'replicas': replica_count}}
        try:
            current_replica = get_current_deployment_scale(
                deployment_name, namespace, client)
            if current_replica != replica_count:
                print(
                    f"Scaling {deployment_name} from {current_replica} to {replica_count}...")
                client.patch_namespaced_deployment_scale(
                    deployment_name, namespace, body)
                print(f"The scale of {deployment_name} succeeded")
        except Exception as err:
            print(
                f"Failed to update {deployment_name} scale to {replica_count}, an error occurred: {err}")
