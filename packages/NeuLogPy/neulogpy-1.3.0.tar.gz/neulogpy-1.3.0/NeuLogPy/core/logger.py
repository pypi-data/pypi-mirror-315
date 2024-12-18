import logging
import coloredlogs

def setup_logger(name):
    """Set up a logger with colored output"""
    logger = logging.getLogger(name)
    
    # Configure coloredlogs
    coloredlogs.install(
        level='INFO',
        logger=logger,
        fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s',
        field_styles={
            'asctime': {'color': 'green'},
            'hostname': {'color': 'magenta'},
            'levelname': {'color': 'cyan', 'bold': True},
            'name': {'color': 'blue'},
            'programname': {'color': 'cyan'},
            'username': {'color': 'yellow'}
        },
        level_styles={
            'debug': {'color': 'blue'},
            'info': {'color': 'green'},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True}
        }
    )
    
    return logger
