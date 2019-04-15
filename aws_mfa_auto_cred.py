import boto3

def get_mfa_credentials():
    """
    Prompt user for mfa token and generate session token
    :return:
    """
    boto3.setup_default_session(profile_name='default')
    iam_client = boto3.client('iam')
    sts_client = boto3.client('sts')
    mfa_device_sn = iam_client.list_mfa_devices()['MFADevices'][0]['SerialNumber']
    mfa_token = raw_input("Please input an aws MFA token: ")
    mfa_credentials = sts_client.get_session_token(
        DurationSeconds=60 * 60 * 8,  # 8hrs
        SerialNumber=mfa_device_sn,
        TokenCode=mfa_token
    )
    return mfa_credentials['Credentials']
