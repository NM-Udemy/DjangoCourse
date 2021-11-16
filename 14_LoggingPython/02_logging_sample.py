import logging

logger = logging.getLogger(__name__)
# loggerの閾値
logger.setLevel(logging.DEBUG)

# handler
s_handler = logging.StreamHandler()
f_handler = logging.FileHandler('logging2.log', encoding='utf-8')

# handler ログレベル
s_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Formatter
s_formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
f_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

# handlerにformatterを設定
s_handler.setFormatter(s_formatter)
f_handler.setFormatter(f_formatter)

# loggerにhandlerを設定
logger.addHandler(s_handler)
logger.addHandler(f_handler)


logger.debug('デバッグログ')
logger.info('インフォログ')
logger.warning('ワーニングログ')
logger.error('エラーログ')
logger.critical('クリティカルログ')

a = 10
b = 0
try:
    c = a / b
except Exception as e:
    logger.error(e, exc_info=True)