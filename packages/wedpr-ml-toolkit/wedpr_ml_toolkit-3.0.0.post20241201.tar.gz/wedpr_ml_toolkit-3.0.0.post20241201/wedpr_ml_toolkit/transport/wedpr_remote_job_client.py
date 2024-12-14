from wedpr_ml_toolkit.transport.wedpr_entrypoint import WeDPREntryPoint
from wedpr_ml_toolkit.common.utils.constant import Constant
from wedpr_ml_toolkit.config.wedpr_ml_config import AuthConfig
from wedpr_ml_toolkit.config.wedpr_ml_config import JobConfig
from wedpr_ml_toolkit.config.wedpr_ml_config import HttpConfig
from wedpr_ml_toolkit.common.utils.base_object import BaseObject
import json
import time
from enum import Enum
from typing import Any


class JobType(Enum):
    PSI = "PSI",
    PREPROCESSING = "PREPROCESSING",
    FEATURE_ENGINEERING = "FEATURE_ENGINEERING",
    XGB_TRAINING = "XGB_TRAINING",
    XGB_PREDICTING = "XGB_PREDICTING"
    LR_TRAINING = "LR_TRAINING",
    LR_PREDICTING = "LR_PREDICTING"


class ModelType(Enum):
    XGB_MODEL_SETTING = "XGB_MODEL_SETTING",
    LR_MODEL_SETTING = "LR_MODEL_SETTING",


class JobStatus(Enum):
    Submitted = "Submitted",
    Running = "Running",
    RunFailed = "RunFailed",
    RunSuccess = "RunSuccess",
    WaitToRetry = "WaitToRetry",
    WaitToKill = "WaitToKill",
    Killing = "Killing",
    Killed = "Killed",
    ChainInProgress = "ChainInProgress"

    def run_success(self) -> bool:
        if self.name == JobStatus.RunSuccess.name:
            return True
        return False

    def run_failed(self) -> bool:
        if self.name == JobStatus.RunFailed.name:
            return True
        return False

    def scheduling(self) -> bool:
        return (not self.run_success()) and (not self.run_failed())

    @staticmethod
    def get_job_status(job_status_tr: str):
        try:
            if job_status_tr is None or len(job_status_tr) == 0:
                return None
            return JobStatus[job_status_tr]
        except:
            return None


class JobInfo(BaseObject):
    def __init__(self, job_id: str = None,
                 job_type: JobType = None,
                 project_id: str = None,
                 param: str = None, **params: Any):
        if job_id is not None:
            self.id = job_id
        self.name = None
        self.owner = None
        self.ownerAgency = None
        self.jobType: str = None
        if job_type is not None:
            self.jobType = job_type.name
        self.parties = None
        self.projectId = project_id
        self.param = param
        self.status = None
        self.result = None
        self.createTime = None
        self.lastUpdateTime = None
        self.set_params(**params)
        self.job_status: JobStatus = JobStatus.get_job_status(self.status)

    def __repr__(self):
        return f"job_id: {self.id}, owner: {self.owner}, ownerAgency: {self.ownerAgency}, " \
               f"jobType: {self.jobType}, status: {self.status}"


class JobParam:
    def __init__(self, job_info: JobInfo, task_parities, dataset_list):
        self.job = job_info.__dict__
        self.taskParties = task_parities
        self.datasetList = dataset_list


class WeDPRResponse(BaseObject):
    def __init__(self, **params: Any):
        self.code = None
        self.msg = None
        self.data = None
        self.set_params(**params)

    def success(self):
        return self.code is not None and self.code == 0


class QueryJobRequest(BaseObject):
    def __init__(self, job_info: JobInfo):
        self.job = job_info

    def as_dict(self):
        result = {}
        if self.job is None:
            return result
        result.update({"job": self.job.as_dict()})
        return result

    def __repr__(self):
        return f"job: {self.job}"


class JobListResponse(BaseObject):
    def __init__(self, **params: Any):
        self.jobs = []
        self.job_object_list = []
        self.total = None
        self.set_params(**params)
        for job_item in self.jobs:
            self.job_object_list.append(JobInfo(**job_item))

    def get_queried_job(self) -> JobInfo:
        if len(self.job_object_list) == 0:
            return None
        return self.job_object_list[0]


class JobDetailResponse(BaseObject):
    def __init__(self, job_info: JobInfo = None, **params: Any):
        self.job: dict = None
        self.job_object: JobInfo = job_info
        self.modelResultDetail: dict = None
        self.resultFileInfo: dict = None
        self.model: dict = None
        self.model_predict_algorithm = {}
        self.set_params(**params)
        if self.job_object is None and self.job is not None:
            self.job_object = JobInfo(**self.job)
        # generate the model_predict algorithm
        if self.model is not None:
            self.model_predict_algorithm.update({"setting": self.model})

    def __repr__(self):
        return f"job: {self.job_object}, modelResultDetail: {self.modelResultDetail}, " \
               f"resultFileInfo: {self.resultFileInfo}, model: {self.model}"


class JobDetailRequest(BaseObject):
    def __init__(self, job_id=None,
                 fetch_job_detail=True,
                 fetch_job_result=True,
                 fetch_log=False):
        self.jobID = job_id
        self.fetchJobDetail = fetch_job_detail
        self.fetchJobResult = fetch_job_result
        self.fetchLog = fetch_log


class WeDPRRemoteJobClient(WeDPREntryPoint, BaseObject):
    def __init__(self, http_config: HttpConfig, auth_config: AuthConfig, job_config: JobConfig):
        if auth_config is None:
            raise Exception("Must define the auth config!")
        if job_config is None:
            raise Exception("Must define the job config")
        super().__init__(auth_config.access_key_id, auth_config.access_key_secret,
                         auth_config.get_remote_entrypoints_list(), http_config, auth_config.nonce_len)
        self.auth_config = auth_config
        self.job_config = job_config

    def get_auth_config(self):
        return self.auth_config

    def get_job_config(self):
        return self.job_config

    def submit_job(self, job_params: JobParam) -> WeDPRResponse:
        wedpr_response = self.send_request(True,
                                           self.job_config.submit_job_uri, None, None, json.dumps(job_params.__dict__))
        submit_result = WeDPRResponse(**wedpr_response)
        # return the job_id
        if submit_result.success():
            return submit_result.data
        raise Exception(
            f"submit_job failed, code: {submit_result.code}, msg: {submit_result.msg}")

    def query_job_detail(self, job_id, block_until_finish) -> JobDetailResponse:
        job_result = self.poll_job_result(job_id, block_until_finish)
        # failed case
        if job_result == None or job_result.job_status == None \
                or (not job_result.job_status.run_success()):
            return JobDetailResponse(job_info=job_result, params=None)
        # success case, query the job detail
        job_detail_requests = JobDetailRequest(job_id)
        response_dict = self.execute_with_retry(self.send_request,
                                                self.job_config.max_retries,
                                                self.job_config.retry_delay_s,
                                                True,
                                                self.job_config.query_job_detail_uri,
                                                None,
                                                None, json.dumps(job_detail_requests.as_dict()))
        wedpr_response = WeDPRResponse(**response_dict)
        if not wedpr_response.success():
            raise Exception(
                f"query_job_detail exception, job: {job_id}, "
                f"code: {wedpr_response.code}, msg: {wedpr_response.msg}")
        return JobDetailResponse(**(wedpr_response.data))

    def poll_job_result(self, job_id, block_until_finish) -> JobInfo:
        while True:
            query_condition = JobInfo(job_id=job_id)
            response_dict = self.execute_with_retry(self.send_request,
                                                    self.job_config.max_retries,
                                                    self.job_config.retry_delay_s,
                                                    True,
                                                    self.job_config.query_job_status_uri,
                                                    None, None,
                                                    json.dumps(QueryJobRequest(job_info=query_condition).as_dict()))
            wedpr_response = WeDPRResponse(**response_dict)
            if not wedpr_response.success():
                raise Exception(
                    f"poll_job_result failed, job_id: {job_id}, code: {wedpr_response.code}, msg: {wedpr_response.msg}")
            # check the result
            result = JobListResponse(**(wedpr_response.data))
            result_job = result.get_queried_job()
            if result_job is None:
                raise Exception(
                    f"poll_job_result for the queried job {job_id} not exists!")
            # run finished
            if result_job.job_status.run_success() or result_job.job_status.run_failed():
                return result_job
            # wait to finish
            if block_until_finish:
                time.sleep(self.job_config.polling_interval_s)
            else:
                return None
