import sys


class CustomException(Exception):
    def __init__(self, message, error_detail: Exception = None):
        _, _, tb = sys.exc_info()
        where = f"{tb.tb_frame.f_code.co_filename}, line {tb.tb_lineno}" if tb else "unknown"
        super().__init__(f"{message} | {where} | {error_detail}")
