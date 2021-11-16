import logging
import logging.config

logging.config.fileConfig(fname='conf/rotation_logger.conf')
logger = logging.getLogger(__name__)

import time
for _ in range(1000):
    logger.debug('デバッグログ')
    logger.info('インフォログ')
    logger.warning('ワーニングログ')
    logger.error('エラーログ')
    logger.critical('クリティカルログ')
    time.sleep(1)
