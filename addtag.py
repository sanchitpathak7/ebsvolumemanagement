import botocore.exceptions
from main import boto_session, time, tag1, tag2, colors
from tags import get_dnd_tag, get_exp_tag


def add_expiration_tag():
    print(colors.HEADER + "Executing script to mark unattached AWS EC2 EBS Volumes with an `Expiration Date` tag:\n")
    try:
        for volume in boto_session().volumes.all():
            print(colors.OKBLUE + "Volume % s:" % volume.volume_id)
            if len(volume.attachments) == 0:
                if tag1 != get_dnd_tag(volume.volume_id):
                    if tag2 != get_exp_tag(volume.volume_id):
                        print(colors.ENDC + "Current tags:", volume.tags)
                        volume.create_tags(Resources=[volume.volume_id],
                                           Tags=[
                                               {
                                                   'Key': 'expiration_date',
                                                   'Value': time()
                                               },
                                           ]
                                           )
                        print(colors.OKGREEN + "Expiration Date tag added. Updated tags -", volume.tags, "\n")
                    else:
                        print(colors.ENDC + "Criteria not met since `Expiration Date` tag present.\n")
                else:
                    print(colors.ENDC + "Criteria not met since `Do Not Delete` tag is present.\n")
            else:
                print(colors.ENDC + "Volume is attached to an instance.\n")
    except botocore.exceptions.ClientError:
        return False, colors.FAIL + "Failed script execution"


add_expiration_tag()
