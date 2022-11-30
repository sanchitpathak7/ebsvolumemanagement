import botocore.exceptions
from main import boto_client, tag1, tag2


def get_dnd_tag(parameter):
    try:
        client = boto_client()
        volumes = client.describe_volumes()
        for volume in volumes['Volumes']:
            if volume['VolumeId'] == parameter:
                try:
                    if volume['Tags'] is not None:
                        for value in volume['Tags']:
                            if value['Key'] == tag1:
                                return value['Key']
                except:
                    return None
    except botocore.exceptions.ClientError:
        return False


def get_exp_tag(parameter):
    try:
        client = boto_client()
        volumes = client.describe_volumes()
        for volume in volumes['Volumes']:
            if volume['VolumeId'] == parameter:
                try:
                    if volume['Tags'] is not None:
                        for value in volume['Tags']:
                            if value['Key'] == tag2:
                                return value['Key']
                except:
                    return None
    except botocore.exceptions.ClientError:
        return False


def get_tags(parameter):
    try:
        client = boto_client()
        volumes = client.describe_volumes()
        for volume in volumes['Volumes']:
            if volume['VolumeId'] == parameter:
                return volume['Tags']
    except botocore.exceptions.ClientError:
        return False
