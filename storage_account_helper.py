from azure.storage.queue import (
    QueueClient
)

def get_queue_length(queue_client):
    """
    Get the approximate length of a given queue client

    Returns
    -------
    count
        The number of the messages in queue
    """
    print(f"Getting the number of messages in {queue_client.queue_name} queue")
    count = None
    try:
        properties = queue_client.get_queue_properties()
        count = properties.approximate_message_count
        print(
            f"The approximate number of mesages in {queue_client.queue_name} is: {count}.")
    except Exception as err:
        print(
            f"Failed to get {queue_client.queue_name} queue approximate length, an error occurred: {err}")

    return count


def get_storage_conn_string(storage_account_name, storage_key):
    """
    Get the storage account connection string
    """
    return f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_key};EndpointSuffix=core.windows.net"


def get_storage_account_queue_client(storage_account, storage_key, queue):
    """
    Get Storage Account queue client
    """
    print(f"Getting {storage_account} storage account connection string...")
    connect_str = get_storage_conn_string(
        storage_account, storage_key)
    print("Getting queue client...")
    queue_client = QueueClient.from_connection_string(
        connect_str, queue)
    return queue_client
