import ibm_boto3
from ibm_botocore.client import Config, ClientError
from django.http import Http404

# Constants for IBM COS credentials
COS_ENDPOINT = "https://s3.ap.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "bVYiq10T-lFdhqANmkgv0g0YN3B3RMWLEEt81U8DmJjr" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/oidc/token"
COS_SERVICE_INSTANCE_ID = "crn:v1:bluemix:public:cloud-object-storage:global:a/422147be0b5a450e863372d024c638b6:fe8d42a9-7de1-41b2-9483-e3b88734c95c::"
BUCKET_NAME = "fame-videos-bucket"

class IBMCOSClient:

    def __init__(self):
        '''initialize configuration'''
        try:
            self.cos = ibm_boto3.client("s3",
                    ibm_api_key_id=COS_API_KEY_ID,
                    ibm_service_instance_id=COS_SERVICE_INSTANCE_ID,
                    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
                    config=Config(signature_version="oauth"),
                    endpoint_url=COS_ENDPOINT
                )
        except:
            print("Set up Client Failed")


    def upload(self, path_to_file,file_name):
        self.cos.upload_file(Filename=path_to_file,Bucket=BUCKET_NAME,Key=file_name)

    def download(self,file_key):
        self.cos.download_file(Filename="../media/{}".format(file_key),Bucket=BUCKET_NAME,Key=file_key)

    def is_key_unique(self,file_key):
        try:
            self.cos.get_object(Bucket=BUCKET_NAME,Key=file_key)
            return False
        except Exception:
            return True