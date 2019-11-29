from src import Something
import logging
import sys

logger = logging.getLogger()

from socket import gethostname
from pythonjsonlogger import jsonlogger

from logging import Filter


class ContextFilter(Filter):
    def __init__(self):
        self._tenant_id: str = "No tenant_id set"
        self._job_id: str = "No job_id set"

    def set_tenant_id(self, tenant_id: str) -> None:
        self._tenant_id = tenant_id

    def set_job_id(self, job_id: str) -> None:
        self._job_id = job_id

    def set_context(self, tenant_id: str, job_id: str) -> None:
        self.set_tenant_id(tenant_id)
        self.set_job_id(job_id)

    def filter(self, record):
        record.tenant_id = self._tenant_id
        record.job_id = self._job_id
        return True


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        if not log_record.get("hostname"):
            log_record["hostname"] = gethostname()


LoggerFormatter = CustomJsonFormatter(
)


class SomeFilter(logging.Filter):

    def filter(self, record):
        record.test = "huhu"
        record.nana = "hähä"
        return True


log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(LoggerFormatter)

logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def main():
    log_filter = ContextFilter()
    log_handler.addFilter(log_filter)
    something = Something()
    something.something()
    log_handler.removeFilter(log_filter)
    logger.error("NANA")


if __name__ == '__main__':
    main()
