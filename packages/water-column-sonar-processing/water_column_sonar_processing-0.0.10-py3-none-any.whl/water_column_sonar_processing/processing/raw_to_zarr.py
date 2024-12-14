import gc
import os
import echopype as ep
import numcodecs
import numpy as np
from numcodecs import Blosc
from datetime import datetime
from pathlib import Path # , PurePath

from water_column_sonar_processing.aws import DynamoDBManager, S3Manager
from water_column_sonar_processing.geometry import GeometryManager
from water_column_sonar_processing.utility import Cleaner

TEMPDIR = "/tmp"


# This code is getting copied from echofish-aws-raw-to-zarr-lambda
class RawToZarr:
    #######################################################
    def __init__(
            self,
            # output_bucket_access_key,
            # output_bucket_secret_access_key,
            # # overwrite_existing_zarr_store,
    ):
        # TODO: revert to Blosc.BITSHUFFLE, troubleshooting misc error
        self.__compressor = Blosc(cname="zstd", clevel=2)  # shuffle=Blosc.NOSHUFFLE
        self.__overwrite = True
        self.__num_threads = numcodecs.blosc.get_nthreads()
        # self.input_bucket_name = os.environ.get("INPUT_BUCKET_NAME")
        # self.output_bucket_name = os.environ.get("OUTPUT_BUCKET_NAME")
        # self.__table_name = table_name
        # # self.__overwrite_existing_zarr_store = overwrite_existing_zarr_store

    ############################################################################
    ############################################################################
    def __zarr_info_to_table(
            self,
            output_bucket_name,
            table_name,
            ship_name,
            cruise_name,
            sensor_name,
            file_name,
            zarr_path,
            min_echo_range,
            max_echo_range,
            num_ping_time_dropna,
            start_time,
            end_time,
            frequencies,
            channels
    ):
        print('Writing Zarr information to DynamoDB table.')
        dynamodb_manager = DynamoDBManager()

        # The problem is that these values were never populated
        # and so when the query looks for values that aren't there
        # they fail
        dynamodb_manager.update_item(
            table_name=table_name,
            key={
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            },
            expression_attribute_names={
                '#CH': 'CHANNELS',
                '#ET': 'END_TIME',
                # "#ED": "ERROR_DETAIL",
                '#FR': 'FREQUENCIES',
                '#MA': 'MAX_ECHO_RANGE',
                '#MI': 'MIN_ECHO_RANGE',
                '#ND': 'NUM_PING_TIME_DROPNA',
                "#PS": "PIPELINE_STATUS",
                "#PT": "PIPELINE_TIME",
                "#SE": "SENSOR_NAME",
                "#SH": "SHIP_NAME",
                '#ST': 'START_TIME',
                '#ZB': 'ZARR_BUCKET',
                '#ZP': 'ZARR_PATH',
            },
            expression_attribute_values={
                ":ch": {"L": [{"S": i} for i in channels]},
                ":et": {"S": end_time},
                # ":ed": {"S": ""},
                ":fr": {"L": [{"N": str(i)} for i in frequencies]},
                ":ma": {"N": str(np.round(max_echo_range, 4))},
                ":mi": {"N": str(np.round(min_echo_range, 4))},
                ":nd": {"N": str(num_ping_time_dropna)},
                ":ps": {"S": "PROCESSING_RESAMPLE_AND_WRITE_TO_ZARR_STORE"},
                ":pt": {"S": datetime.now().isoformat(timespec="seconds") + "Z"},
                ":se": {"S": sensor_name},
                ":sh": {"S": ship_name},
                ":st": {"S": start_time},
                ":zb": {"S": output_bucket_name},
                ":zp": { "S": zarr_path },
            },
            update_expression=(
                "SET "
                "#CH = :ch, "
                "#ET = :et, "
                # "#ED = :ed, "
                "#FR = :fr, "
                "#MA = :ma, "
                "#MI = :mi, "
                "#ND = :nd, "
                "#PS = :ps, "
                "#PT = :pt, "
                "#SE = :se, "
                "#SH = :sh, "
                "#ST = :st, "
                "#ZB = :zb, "
                "#ZP = :zp"
            ),
        )

    ############################################################################
    ############################################################################
    ############################################################################
    def __upload_files_to_output_bucket(
            self,
            output_bucket_name,
            local_directory,
            object_prefix,
    ):
        # Note: this will be passed credentials if using NODD
        s3_manager = S3Manager()
        print('Uploading files using thread pool executor.')
        all_files = []
        for subdir, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                s3_key = os.path.join(object_prefix, local_path)
                all_files.append([local_path, s3_key])
        # all_files
        all_uploads = s3_manager.upload_files_with_thread_pool_executor(
            output_bucket_name=output_bucket_name,
            all_files=all_files,
        )
        return all_uploads

    ############################################################################
    def raw_to_zarr(
            self,
            table_name,
            output_bucket_name,
            ship_name,
            cruise_name,
            sensor_name,
            raw_file_name,
    ):
        """
        Downloads the raw files, processes them with echopype, writes geojson, and uploads files
        to the nodd bucket.
        """
        print(f'Opening raw: {raw_file_name} and creating zarr store.')
        geometry_manager = GeometryManager()
        cleaner = Cleaner()
        cleaner.delete_local_files(file_types=["*.zarr", "*.json"]) # TODO: include bot and raw?
        try:
            gc.collect()
            print('Opening raw file with echopype.')
            # s3_file_path = f"s3://{bucket_name}/data/raw/{ship_name}/{cruise_name}/{sensor_name}/{file_name}"
            # s3_file_path = Path(f"s3://noaa-wcsd-pds/data/raw/{ship_name}/{cruise_name}/{sensor_name}/{file_name}")
            echodata = ep.open_raw(
                raw_file=raw_file_name,
                sonar_model=sensor_name,
                include_bot=True,
                use_swap=True,
                # max_chunk_size=100,
                # storage_options={'anon': True } # 'endpoint_url': self.endpoint_url} # this was creating problems
            )
            print('Compute volume backscattering strength (Sv) from raw data.')
            ds_sv = ep.calibrate.compute_Sv(echodata)
            print('Done computing volume backscattering strength (Sv) from raw data.')
            frequencies = echodata.environment.frequency_nominal.values
            #################################################################
            # Get GPS coordinates
            gps_data, lat, lon = geometry_manager.read_echodata_gps_data(
                echodata=echodata,
                output_bucket_name=output_bucket_name,
                ship_name=ship_name,
                cruise_name=cruise_name,
                sensor_name=sensor_name,
                file_name=raw_file_name,
                write_geojson=True
            )
            # gps_data, lat, lon = self.__get_gps_data(echodata=echodata)
            #################################################################
            # Technically the min_echo_range would be 0 m.
            # TODO: this var name is supposed to represent minimum resolution of depth measurements
            # TODO revert this so that smaller diffs can be used
            # The most minimum the resolution can be is as small as 0.25 meters
            min_echo_range = np.maximum(
                0.25,
                np.nanmin(np.diff(ds_sv.echo_range.values))
            )
            max_echo_range = float(np.nanmax(ds_sv.echo_range))
            #
            num_ping_time_dropna = lat[~np.isnan(lat)].shape[0]  # symmetric to lon
            #
            start_time = np.datetime_as_string(ds_sv.ping_time.values[0], unit='ms') + "Z"
            end_time = np.datetime_as_string(ds_sv.ping_time.values[-1], unit='ms') + "Z"
            channels = list(ds_sv.channel.values)
            #
            #################################################################
            # Create the zarr store
            store_name = f"{Path(raw_file_name).stem}.zarr"
            ds_sv.to_zarr(store=store_name)
            #################################################################
            output_zarr_prefix = f"level_1/{ship_name}/{cruise_name}/{sensor_name}/"
            #################################################################
            # If zarr store already exists then delete
            s3_manager = S3Manager()
            child_objects = s3_manager.get_child_objects(
                bucket_name=output_bucket_name,
                sub_prefix=f"level_1/{ship_name}/{cruise_name}/{sensor_name}/{Path(raw_file_name).stem}.zarr",
            )
            if len(child_objects) > 0:
                print('Zarr store data already exists in s3, deleting existing and continuing.')
                s3_manager.delete_nodd_objects(
                    bucket_name=output_bucket_name,
                    objects=child_objects,
                )
            #################################################################
            self.__upload_files_to_output_bucket(
                output_bucket_name=output_bucket_name,
                local_directory=store_name,
                object_prefix=output_zarr_prefix
            )
            #################################################################
            self.__zarr_info_to_table(
                output_bucket_name=output_bucket_name,
                table_name=table_name,
                ship_name=ship_name,
                cruise_name=cruise_name,
                sensor_name=sensor_name,
                file_name=raw_file_name,
                zarr_path=os.path.join(output_zarr_prefix, store_name),
                min_echo_range=min_echo_range,
                max_echo_range=max_echo_range,
                num_ping_time_dropna=num_ping_time_dropna,
                start_time=start_time,
                end_time=end_time,
                frequencies=frequencies,
                channels=channels
            )
            #######################################################################
            # TODO: verify count of objects matches, publish message, update status
            #######################################################################
            print('here')
        except Exception as err:
            print(f'Exception encountered creating local Zarr store with echopype: {err}')
            raise RuntimeError(f"Problem creating local Zarr store, {err}")
        finally:
            cleaner.delete_local_files(file_types=["*.raw", "*.bot", "*.zarr", "*.json"])
        print('Done creating local zarr store.')

    ############################################################################
    # TODO: does this get called?
    # def execute(self, input_message):
    #     ship_name = input_message['shipName']
    #     cruise_name = input_message['cruiseName']
    #     sensor_name = input_message['sensorName']
    #     input_file_name = input_message['fileName']
    #     #
    #     try:
    #         self.__update_processing_status(
    #             file_name=input_file_name,
    #             cruise_name=cruise_name,
    #             pipeline_status="PROCESSING_RAW_TO_ZARR"
    #         )
    #         #######################################################################
    #         store_name = f"{os.path.splitext(input_file_name)[0]}.zarr"
    #         output_zarr_prefix = f"level_1/{ship_name}/{cruise_name}/{sensor_name}"
    #         bucket_key = f"data/raw/{ship_name}/{cruise_name}/{sensor_name}/{input_file_name}"
    #         zarr_prefix = os.path.join("level_1", ship_name, cruise_name, sensor_name)
    #         #
    #         os.chdir(TEMPDIR)  # Lambdas require use of temp directory
    #         #######################################################################
    #         #######################################################################
    #         # Check if zarr store already exists
    #         s3_objects = self.__s3.list_objects(
    #             bucket_name=self.__output_bucket,
    #             prefix=f"{zarr_prefix}/{os.path.splitext(input_file_name)[0]}.zarr/",
    #             access_key_id=self.__output_bucket_access_key,
    #             secret_access_key=self.__output_bucket_secret_access_key
    #         )
    #         if len(s3_objects) > 0:
    #             print('Zarr store data already exists in s3, deleting existing and continuing.')
    #             self.__s3.delete_objects(
    #                 bucket_name=self.__output_bucket,
    #                 objects=s3_objects,
    #                 access_key_id=self.__output_bucket_access_key,
    #                 secret_access_key=self.__output_bucket_secret_access_key
    #             )
    #         #######################################################################
    #         # self.__delete_all_local_raw_and_zarr_files()
    #         Cleaner.delete_local_files(file_types=["*.raw*", "*.zarr"])
    #         self.__s3.download_file(
    #             bucket_name=self.__input_bucket,
    #             key=bucket_key,
    #             file_name=input_file_name
    #         )
    #         self.__create_local_zarr_store(
    #             raw_file_name=input_file_name,
    #             cruise_name=cruise_name,
    #             sensor_name=sensor_name,
    #             output_zarr_prefix=output_zarr_prefix,
    #             store_name=store_name
    #         )
    #         #######################################################################
    #         self.__upload_files_to_output_bucket(store_name, output_zarr_prefix)
    #         #######################################################################
    #         # # TODO: verify count of objects matches
    #         # s3_objects = self.__s3.list_objects(
    #         #     bucket_name=self.__output_bucket,
    #         #     prefix=f"{zarr_prefix}/{os.path.splitext(input_file_name)[0]}.zarr/",
    #         #     access_key_id=self.__output_bucket_access_key,
    #         #     secret_access_key=self.__output_bucket_secret_access_key
    #         # )
    #         #######################################################################
    #         self.__update_processing_status(
    #             file_name=input_file_name,
    #             cruise_name=cruise_name,
    #             pipeline_status='SUCCESS_RAW_TO_ZARR'
    #         )
    #         #######################################################################
    #         self.__publish_done_message(input_message)
    #         #######################################################################
    #     # except Exception as err:
    #     #     print(f'Exception encountered: {err}')
    #     # self.__update_processing_status(
    #     #     file_name=input_file_name,
    #     #     cruise_name=cruise_name,
    #     #     pipeline_status='FAILURE_RAW_TO_ZARR',
    #     #     error_message=str(err),
    #     # )
    #     finally:
    #         self.__delete_all_local_raw_and_zarr_files()
    #######################################################################

    ############################################################################

################################################################################
############################################################################
