from pirupy import *

callStack=''
###
@pipeline(stages=("first_stage","second_stage","third_stage"))
def aTypicalPipeline(env:dict = {}):
    global callStack
    callStack='aTypicalPipeline:'
    return env

# A stage is constitued by @jobs for the matching stage,
# in the order that they will be found while introspecting the class (no guaranteed order)
@job(stage="first_stage")
def B(*, env:dict = {}):
    global callStack
    callStack += 'B'
    pass

@job(stage="first_stage")
def A(*, env:dict = {}):
    global callStack
    callStack += 'A'
    pass

@job(stage="second_stage")
def C(*, env:dict = {}):
    global callStack
    callStack += 'C'
    pass

@job(stage="second_stage")
def F(*, env:dict = {}):
    global callStack
    callStack += 'F'
    pass

@job(stage="third_stage")
def E(*, env:dict = {}):
    global callStack
    callStack += 'E'
    pass

@job(stage="second_stage")
def D(*, env:dict = {}):
    global callStack
    callStack += 'D'
    pass

@job(stage="third_stage")
def G(*, env:dict = {}):
    global callStack
    callStack += 'G'
    pass

@job()
def H(*, env:dict = {}): # performed at each stage
    global callStack
    callStack += 'H'
    pass

@before_all
def setup(*, env:dict = {}):
    global callStack
    callStack += '(su)'
    pass

@after_all
def teardown(*, env:dict = {}):
    global callStack
    callStack += '(td)'
    pass

@before_each(stage="first_stage")
def enter_first_stage_job(*, env:dict = {}): # called only before performing each job of a given stage
    global callStack
    callStack += '(efs)'
    pass

@after_each
def exit_job(*, env:dict = {}): # called after each jobs has been called during any stage.
    global callStack
    callStack += '(x)'
    pass

def test_that_pipeline_call_functions_in_expected_order():
    aTypicalPipeline()
    assert callStack == 'aTypicalPipeline:(su)(efs)B(x)(efs)A(x)(efs)H(x)C(x)F(x)D(x)H(x)E(x)G(x)H(x)(td)'
