#!/usr/bin/env python

import boto3
import yaml
import datetime
import botocore.exceptions


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open("creds.yaml", "r") as target:
    r = yaml.safe_load(target)
    access_key_id = r['aws']['platform9-support']['access_key_id']
    secret_access_key = r['aws']['platform9-support']['secret_key_id']
    region_name = r['aws']['platform9-support']['region_name']
tag1 = 'do_not_delete'
tag2 = 'expiration_date'
url = 'https://hooks.slack.com/services/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'


def time():
    current_date = datetime.datetime.now().timestamp()
    expiration_duration = datetime.datetime.fromtimestamp(current_date) + datetime.timedelta(seconds=604800)
    expiration_date = expiration_duration.timestamp()
    return str(int(expiration_date))


def boto_session():
    if access_key_id is None:
        raise ValueError('AWS access_key cannot be None!')
    if secret_access_key is None:
        raise ValueError('AWS secret_key cannot be None!')
    if region_name is None:
        raise ValueError('AWS region cannot be None!')
    session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                            region_name=region_name)
    try:
        session.resource('ec2')
    except botocore.exceptions.ClientError as e:
        return False, 'Access key id or secret access key could not be authenticated'
    except botocore.exceptions.EndpointConnectionError as e:
        return False, 'Could not connect to AWS'
    return session.resource('ec2')


def boto_client():
    if access_key_id is None:
        raise ValueError('AWS access_key cannot be None!!')
    if secret_access_key is None:
        raise ValueError('AWS secret_key cannot be None!!')
    if region_name is None:
        raise ValueError('AWS region cannot be None!!')
    client = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                          region_name=region_name)
    return client
