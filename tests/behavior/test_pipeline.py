from pirupy import *

callStack=''
###
@pipeline(stages=("first_stage","second_stage","third_stage"))
def aTypicalPipeline(env:dict = {}):
    global callStack
    callStack='aTypicalPipeline:'
    assert(env['a'] == 'from the pipeline launcher')
    env['b']='from the pipeline'
    return env

# A stage is constitued by @jobs for the matching stage,
# in the order that they will be found while introspecting the class (no guaranteed order)
@job(stage="first_stage")
def B(*, env:dict = {}):
    global callStack
    callStack += 'B'
    assert(list(env.keys()) == ['a','b','c','d'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    assert(env['d'] == 'from enter_first_stage_job')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job(stage="first_stage")
def A(*, env:dict = {}):
    global callStack
    callStack += 'A'
    assert(list(env.keys()) == ['a','b','c','d'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    assert(env['d'] == 'from enter_first_stage_job')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job(stage="second_stage")
def C(*, env:dict = {}):
    global callStack
    callStack += 'C'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job(stage="second_stage")
def F(*, env:dict = {}):
    global callStack
    callStack += 'F'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job(stage="third_stage")
def E(*, env:dict = {}):
    global callStack
    callStack += 'E'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job(stage="second_stage")
def D(*, env:dict = {}):
    global callStack
    callStack += 'D'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job(stage="third_stage")
def G(*, env:dict = {}):
    global callStack
    callStack += 'G'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@job()
def H(*, env:dict = {}): # performed at each stage
    global callStack
    callStack += 'H'
    assert(list(env.keys()) == ['a','b','c','d'] or list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    if 'd' in env:
        assert(env['d'] == 'from enter_first_stage_job')
    env['a'] = 'overwritten a'
    env['d'] = 'overwritten d'
    pass

@before_all
def set_up(*, env:dict = {}): # 'setup' function name already reserved by pytest...
    global callStack
    callStack += '(su)'
    assert(list(env.keys()) == ['a','b'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    env['c'] = 'from setup'
    pass

@after_all
def tear_down(*, env:dict = {}):
    global callStack
    callStack += '(td)'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    pass

@before_each(stage="first_stage")
def enter_first_stage_job(*, env:dict = {}): # called only before performing each job of a given stage
    global callStack
    callStack += '(efs)'
    assert(list(env.keys()) == ['a','b','c'])
    assert(env['a'] == 'from the pipeline launcher')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    env['d'] = 'from enter_first_stage_job'
    pass

@after_each
def exit_job(*, env:dict = {}): # called after each jobs has been called during any stage.
    global callStack
    callStack += '(x)'
    assert(list(env.keys()) == ['a','b','c','d'])
    assert(env['a'] == 'overwritten a')
    assert(env['b'] == 'from the pipeline')
    assert(env['c'] == 'from setup')
    assert(env['d'] == 'overwritten d')
    env['b'] = 'overwritten c'
    pass

def test_that_pipeline_works_as_expected():
    aTypicalPipeline({'a':'from the pipeline launcher'})
    assert callStack == 'aTypicalPipeline:(su)(efs)B(x)(efs)A(x)(efs)H(x)C(x)F(x)D(x)H(x)E(x)G(x)H(x)(td)'
