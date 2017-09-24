def get_mfa_credentials(tag=None):
    mfa_device_info_list = local('aws iam list-mfa-devices', capture=True)
    mfa_device_arn = json.loads(mfa_device_info_list)['MFADevices'][0]['SerialNumber']
    mfa_token = raw_input("Please input an aws MFA token: ")
    
    credentials = local('aws sts get-session-token --serial-number ' + mfa_device_arn + ' --token-code ' + mfa_token, capture=True)
    credentail_data = json.loads(credentials)['Credentials']  
    cred_file = open(os.path.join(os.path.expanduser('~'),'.aws/credentials'), 'r')
    creds = cred_file.read()
    open(os.path.join(os.path.expanduser('~'),'.aws/credentials'), 'w').close()
    write_creads = open(os.path.join(os.path.expanduser('~'),'.aws/credentials'), 'w')

    if "[mfa-role]" in creds:
        default_creds =  creds.split("[mfa-role]", 1)[0]
        write_creds.write(default_creds)  
        write_creds.write("[mfa-role]\n")
        write_creds.write("\n")
        write_creds.write("aws_access_key_id = " + credentail_data['AccessKeyId'] + "\n")
        write_creds.write("aws_secret_access_key = " + credentail_data['SecretAccessKey'] + "\n")
        write_creds.write("aws_session_token = " + credentail_data['SessionToken'] + "\n")
    else:
        write_creds.truncate()
        write_creds.write(creds)
        write_creds.write("[mfa-role]\n")
        write_creds.write("\n")
        write_creds.write("aws_access_key_id = " + credentail_data['AccessKeyId'] + "\n")
        write_creds.write("aws_secret_access_key = " + credentail_data['SecretAccessKey'] + "\n")
        write_creds.write("aws_session_token = " + credentail_data['SessionToken'] + "\n")

    return credentail_data
