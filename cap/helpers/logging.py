from logging import DEBUG
import colorlog


# Patch logger.info to behave like print
def patch_logger_info(_logger):
    original_logger_info = _logger.info
    def __info(*args, **kwargs):
        original_logger_info(' '.join([str(arg) for arg in args]), **kwargs)
    return __info

def patch_logger_warn(_logger):
    original_logger_warn = _logger.warn
    def __warn(*args, **kwargs):
        original_logger_warn(' '.join([str(arg) for arg in args]), **kwargs)
    return __warn

# NOTE: Here's the default color for colorlog
# The default colors to use for the debug levels
# default_log_colors = {
#     "DEBUG": "white",
#     "INFO": "green",
#     "WARNING": "yellow",
#     "ERROR": "red",
#     "CRITICAL": "bold_red",
# }
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(levelname)s] %(name)s: %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger('cap')
logger.addHandler(handler)
logger.setLevel(DEBUG)

logger.info = patch_logger_info(logger)
logger.warn = patch_logger_warn(logger)