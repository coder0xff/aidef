import logging

def getlogger(name, handler=None):
    log = logging.getLogger(name)
    log.addHandler(handler or logging.StreamHandler())
    # set the logger to print the time
    log.handlers[0].setFormatter(logging.Formatter("%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))
    # set the loggers datetime format
    log.handlers[0].formatter.datefmt = "%Y-%m-%d:%H:%M:%S"
    return log