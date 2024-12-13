import json
import os
import boto3
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from boto3.s3.transfer import TransferConfig
from botocore.config import Config
from botocore.exceptions import ClientError

MAX_POOL_CONNECTIONS = 64
MAX_CONCURRENCY = 64
MAX_WORKERS = 64
GB = 1024**3


#########################################################################
def chunked(ll: list, n: int) -> Generator:
    # Yields successively n-sized chunks from ll.
    for i in range(0, len(ll), n):
        yield ll[i : i + n]


class S3Manager:
    #####################################################################
    def __init__(
        self,
        # input_endpoint_url: str,
        # output_endpoint_url: str,
        # endpoint_url
        # TODO: Need to allow passing in of credentials when writing to protected bucket
    ):
        self.input_bucket_name = os.environ.get("INPUT_BUCKET_NAME")
        self.output_bucket_name = os.environ.get("OUTPUT_BUCKET_NAME")
        # self.endpoint_url = endpoint_url
        # self.input_endpoint_url = input_endpoint_url
        # self.output_endpoint_url = output_endpoint_url
        self.s3_region = os.environ.get("AWS_REGION", default="us-east-1")
        self.s3_client_config = Config(max_pool_connections=MAX_POOL_CONNECTIONS)
        self.s3_transfer_config = TransferConfig(
            max_concurrency=MAX_CONCURRENCY,
            use_threads=True,
            max_bandwidth=None,
            multipart_threshold=10 * GB,
        )
        self.s3_session = boto3.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
            region_name=self.s3_region,
        )
        self.s3_client = self.s3_session.client(
            service_name="s3",
            config=self.s3_client_config,
            region_name=self.s3_region,
            # endpoint_url=endpoint_url, # TODO: temporary
        )
        self.s3_resource = boto3.resource(
            service_name="s3",
            config=self.s3_client_config,
            region_name=self.s3_region,
        )
        # self.paginator = self.s3_client.get_paginator(operation_name='list_objects_v2')
        self.s3_session_noaa_wcsd_zarr_pds = boto3.Session(
            aws_access_key_id=os.environ.get("OUTPUT_BUCKET_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("OUTPUT_BUCKET_SECRET_ACCESS_KEY"),
            region_name=self.s3_region,
        )
        self.s3_client_noaa_wcsd_zarr_pds = self.s3_session_noaa_wcsd_zarr_pds.client(
            service_name="s3",
            config=self.s3_client_config,
            region_name=self.s3_region,
            # endpoint_url=endpoint_url, # TODO: temporary
        )
        self.s3_resource_noaa_wcsd_zarr_pds = self.s3_session_noaa_wcsd_zarr_pds.resource(
            service_name="s3",
            config=self.s3_client_config,
            region_name=self.s3_region,
        )
        self.paginator = self.s3_client.get_paginator('list_objects_v2')
        self.paginator_noaa_wcsd_zarr_pds = self.s3_client_noaa_wcsd_zarr_pds.get_paginator('list_objects_v2')

    def get_client(self): # TODO: do i need this?
        return self.s3_session.client(
            service_name="s3",
            config=self.s3_client_config,
            region_name=self.s3_region,
        )

    #####################################################################
    def create_bucket(
        self,
        bucket_name: str,
    ):
        self.s3_client.create_bucket(
            Bucket=bucket_name,
            # Required when region is different then us-east-1
            #
            # TODO: if region is us-east-1, don't include this line somehow
            # CreateBucketConfiguration={'LocationConstraint': self.__s3_region}
        )

    #####################################################################
    def list_buckets(self):
        # client = self.get_client()
        client = self.s3_client
        return client.list_buckets()

    #####################################################################
    def upload_nodd_file(
        self,
        file_name: str,
        key: str,
        output_bucket_name: str,
    ):
        """
        Used to upload a single file, e.g. the GeoJSON file to the NODD bucket
        """
        self.s3_resource_noaa_wcsd_zarr_pds.Bucket(output_bucket_name).upload_file(Filename=file_name, Key=key)
        return key

    #####################################################################
    def upload_files_with_thread_pool_executor(
        self,
        output_bucket_name: str,
        all_files: list,
    ):
        # 'all_files' is passed a list of lists: [[local_path, s3_key], [...], ...]
        all_uploads = []
        try:  # TODO: problem with threadpool here, missing child files
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [
                    executor.submit(
                        self.upload_nodd_file,  # TODO: verify which one is using this
                        all_file[0],  # file_name
                        all_file[1],  # key
                        output_bucket_name,  # output_bucket_name
                    )
                    for all_file in all_files
                ]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        all_uploads.extend([result])
        except Exception as err:
            print(err)
        print("Done uploading files using threading pool.")
        return all_uploads

    #####################################################################
    # def upload_nodd_file2(
    #         self,
    #         body: str,
    #         bucket: str,
    #         key: str,
    # ):
    #     self.s3_client_noaa_wcsd_zarr_pds.put_object(
    #         Body=body,
    #         Bucket=bucket,
    #         Key=key,
    #     )

    # TODO: this uses resource, try to use client
    def upload_file(
            self,
            filename: str,
            bucket_name: str,
            key: str,
    ):
        # self.s3_client.upload_file(Filename=filename, Bucket=bucket, Key=key)
        self.s3_resource.Bucket(bucket_name).upload_file(Filename=filename, Key=key)

    #####################################################################
    def upload_zarr_files_to_bucket(  # noaa-wcsd-model-pds
        self,
        local_directory,
        remote_directory,
    ):
        # Right now this is just for uploading a model store to s3
        print("Uploading files to output bucket.")
        store_name = os.path.basename(local_directory)
        all_files = []
        for subdir, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                # s3_key = os.path.join(object_prefix, local_path)
                s3_key = os.path.join(
                    remote_directory,
                    store_name,
                    subdir.split(store_name)[-1].strip("/"),
                )
                all_files.append([local_path, s3_key])

        all_uploads = self.upload_files_with_thread_pool_executor(
            all_files=all_files,
        )
        print("Done uploading files to output bucket.")
        return all_uploads

    #####################################################################
    # used: raw-to-zarr
    def list_objects(  # noaa-wcsd-pds and noaa-wcsd-zarr-pds
        self,
        bucket_name,
        prefix
    ):
        # analog to "find_children_objects"
        # Returns a list of key strings for each object in bucket defined by prefix
        # s3_client = self.s3_client
        keys = []
        # paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = self.paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in page_iterator:
            if "Contents" in page.keys():
                keys.extend([k["Key"] for k in page["Contents"]])
        return keys

    # def list_nodd_objects(  # These are used by the geometry for uploading data
    #     self,
    #     prefix,
    # ):
    #     # Returns a list of key strings for each object in bucket defined by prefix
    #     keys = []
    #     page_iterator = self.paginator_noaa_wcsd_zarr_pds.paginate(Bucket=self.output_bucket_name, Prefix=prefix):
    #     for page in paginator.paginate(Bucket=self.output_bucket_name, Prefix=prefix):
    #         if "Contents" in page.keys():
    #             keys.extend([k["Key"] for k in page["Contents"]])
    #     return keys

    #####################################################################
    # TODO: change name to "directory"
    def folder_exists_and_not_empty(self, bucket_name: str, path: str) -> bool:
        if not path.endswith("/"):
            path = path + "/"
        s3_client = self.s3_client
        resp = self.list_objects(
            bucket_name=bucket_name, prefix=path
        )  # TODO: this is returning root folder and doesn't include children or hidden folders
        # resp = s3_client.list_objects(Bucket=bucket, Prefix=path, Delimiter='/', MaxKeys=1)
        return "Contents" in resp

    #####################################################################
    # used
    def __paginate_child_objects(
        self,
        bucket_name: str,
        sub_prefix: str = None,
    ) -> list:
        page_iterator = self.s3_client.get_paginator("list_objects_v2").paginate(
            Bucket=bucket_name, Prefix=sub_prefix
        )
        objects = []
        for page in page_iterator:
            if "Contents" in page.keys():
                objects.extend(page["Contents"])
        return objects

    def get_child_objects(
        self,
        bucket_name: str,
        sub_prefix: str,
        file_suffix: str = None,
    ) -> list:
        print("Getting child objects")
        raw_files = []
        try:
            children = self.__paginate_child_objects(
                bucket_name=bucket_name,
                sub_prefix=sub_prefix,
            )
            if file_suffix is None:
                raw_files = children
            else:
                for child in children:
                    # Note: Any files with predicate 'NOISE' are to be ignored
                    # see: "Bell_M._Shimada/SH1507" cruise for more details.
                    if child["Key"].endswith(file_suffix) and not os.path.basename(
                        child["Key"]
                    ).startswith("NOISE"):
                        raw_files.append(child["Key"])
                return raw_files
        except ClientError as err:
            print(f"Problem was encountered while getting s3 files: {err}")
            raise
        print(f"Found {len(raw_files)} files.")
        return raw_files

    #####################################################################
    def get_object(  # TODO: Move this to index.py
        # noaa-wcsd-pds or noaa-wcsd-model-pds
        self,
        bucket_name,
        key_name,
    ):
        # Meant for getting singular objects from a bucket, used by indexing lambda
        print(f"Getting object {key_name} from {bucket_name}")
        try:
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=key_name,
            )
            # status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
            # if status == 200:
        except ClientError as err:
            print(f"Problem was encountered while getting s3 file: {err}")
            raise
        print(f"Done getting object {key_name} from {bucket_name}")
        return response

    #####################################################################
    # used raw-to-model
    def download_file(  # TODO: change to download_object
        # noaa-wcsd-pds or noaa-wcsd-model-pds
        self,
        bucket_name,
        key,
        file_name, # where the file will be saved
    ):
        self.s3_client.download_file(Bucket=bucket_name, Key=key, Filename=file_name)
        # TODO: if bottom file doesn't exist, don't fail downloader
        print("downloaded file")

    #####################################################################
    # not used
    # def delete_nodd_object(  # noaa-wcsd-model-pds
    #         self,
    #         bucket_name,
    #         key
    # ):  # -> dict:
    #     #return self.__s3_client.delete_object(Bucket=bucket_name, Key=key)
    #     self.s3_client.delete_object(Bucket=bucket_name, Key=key)

    #####################################################################
    def delete_nodd_objects(  # nodd-bucket
        self,
        objects: list,
    ):
        try:
            print(
                f"Deleting {len(objects)} objects in {self.output_bucket_name} in batches."
            )
            objects_to_delete = []
            for obj in objects:
                objects_to_delete.append({"Key": obj["Key"]})
            # Note: request can contain a list of up to 1000 keys
            for batch in chunked(ll=objects_to_delete, n=1000):
                self.s3_client_noaa_wcsd_zarr_pds.delete_objects(
                    Bucket=self.output_bucket_name, Delete={"Objects": batch}
                )
            print(f"Deleted files.")
        except Exception as err:
            print(f"Problem was encountered while deleting objects: {err}")

    #####################################################################
    # not used TODO: remove
    def put(self, bucket_name, key, body):  # noaa-wcsd-model-pds
        self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=body) # "Body" can be a file

    #####################################################################
    def read_s3_json(
        self,
        ship_name,
        cruise_name,
        sensor_name,
        file_name_stem,
    ) -> str:
        try:
            content_object = self.s3_resource_noaa_wcsd_zarr_pds.Object(
                bucket_name=self.output_bucket_name,
                key=f"spatial/geojson/{ship_name}/{cruise_name}/{sensor_name}/{file_name_stem}.json",
            ).get()
            file_content = content_object["Body"].read().decode("utf-8")
            json_content = json.loads(file_content)
            return json_content
        except Exception as err:  # Failure
            print(f"Exception encountered reading s3 GeoJSON: {err}")
            raise

    #####################################################################


#########################################################################
