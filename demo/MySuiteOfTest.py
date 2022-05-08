from pirupy import *
import logging
import logging.config

# setup logging
logging.config.fileConfig('logging.ini')

###
@pipeline(stages=("first_stage","second_stage","third_stage"))
def performMySuiteOfTests(env:dict = {}):
    logging.info("Start of pipeline -- init")
    logging.debug(env)
    return env

# A stage is constitued by @jobs for the matching stage,
# in the order that they will be found while introspecting the class (no guaranteed order)
@job(stage="first_stage")
def B(*, env:dict = {}):
    logging.info("performing... B")
    pass

@job(stage="first_stage")
def A(*, env:dict = {}):
    logging.info("performing... A")
    pass

@job(stage="second_stage")
def C(*, env:dict = {}):
    logging.info("performing... C")
    pass

@job(stage="second_stage")
def F(*, env:dict = {}):
    logging.info("performing... F")
    pass

@job(stage="third_stage")
def E(*, env:dict = {}):
    logging.info("performing... E")
    pass

@job(stage="second_stage")
def D(*, env:dict = {}):
    logging.info("performing... D")
    pass

@job(stage="third_stage")
def G(*, env:dict = {}):
    logging.info("performing... G")
    pass

@job()
def H(*, env:dict = {}): # performed at each stage
    logging.info("performing... H")
    pass

@before_all
def setup(*, env:dict = {}):
    logging.info("performing... setup")
    pass

@after_all
def teardown(*, env:dict = {}):
    logging.info("performing... teardown")
    pass

@before_each(stage="first_stage")
def enter_first_stage_job(*, env:dict = {}): # called only before performing each job of a given stage
    logging.info("performing... enter_first_stage_job")
    pass

@after_each
def exit_job(*, env:dict = {}): # called after each jobs has been called during any stage.
    logging.info("performing... exit_job")
    pass

### demo
if __name__ == "__main__":
    logging.warn("before calling pipeline")
    performMySuiteOfTests(env={'dir.current':'this/path', 'dir.basedir':'that/path'})
    logging.warn("after calling pipeline")
