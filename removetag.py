import botocore.exceptions
from main import boto_client, tag1, tag2, colors
from tags import get_dnd_tag, get_exp_tag, get_tags


def remove_expiration_tag():
    print(colors.HEADER + "Executing script to remove `Expiration Date` tag from recently attached "
                          "AWS EC2 EBS Volumes having a `Do Not Delete` tag:\n")
    try:
        client = boto_client()
        volumes = client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['in-use']}])
        for volume in volumes['Volumes']:
            print(colors.OKBLUE + "Volume %s:" % volume['VolumeId'])
            if len(volume['Attachments']) >= 1:
                if tag1 == get_dnd_tag(volume['VolumeId']):
                    if tag2 == get_exp_tag(volume['VolumeId']):
                        print(colors.ENDC + "Current tags:", volume['Tags'])
                        client.delete_tags(
                            Resources=[
                                str(volume['VolumeId']), ],
                            Tags=[
                                {
                                    'Key': 'expiration_date',
                                },
                            ]
                        )
                        print(colors.OKGREEN + "Expiration Date tag removed. Updated tags:", get_tags(volume['VolumeId']), "\n")
                    else:
                        print(colors.ENDC + "Criteria not met since `Expiration Date` tag is not present.\n")
                else:
                    print(colors.ENDC + "Criteria not met since `Do Not Delete` tag is not present.\n")
            else:
                print(colors.ENDC + "Volume is currently not in use.\n")
    except botocore.exceptions.ClientError:
        return False, colors.FAIL + "Failed script execution"


remove_expiration_tag()
