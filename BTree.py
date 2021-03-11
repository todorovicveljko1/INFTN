from functools import partial, wraps
import inspect
 #
RUNNING = "RUNNING"
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"


class BehaveException(Exception):
    pass


class Blackboard(object):
    def __init__(self, node, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.tick = self.new_iterator(node)
        self.next = self.repeat_iterator(node)

    def new_iterator(self, node):
        it = node.Iterator(self, node)
        it.done = False

        def it_func():
            if it.done:
                raise BehaveException("Ticking a finished node.")
            x = it()
            if x != RUNNING:
                it.done = True
            return x

        return it_func

    def repeat_iterator(self, node):
        it = node.Iterator(self, node)
        return it

class Node:
    def __init__(self):
        self._name = None 
    
    def blackboard(self, *args, **kwargs):
        return Blackboard(self, *args, **kwargs)

class ActionNode(Node):
    def __init__(self, _func = None):
        self.func = _func
    
    class Iterator(object):
        def __init__(self, bb, node):
            self.func = partial(node.func, *bb.args, **bb.kwargs)

        def __call__(self):
            x = self.func()
            if x is None:
                return SUCCESS
            assert x == SUCCESS or x == FAILURE or x == RUNNING
            return x

class ConditionNode(Node):
    def __init__(self, _func = None):
        self.func = _func

    class Iterator(object):
        def __init__(self, bb, node):
            self.func = partial(node.func, *bb.args, **bb.kwargs)

        def __call__(self):
            return SUCCESS if self.func() else FAILURE

class SequenceNode(Node):
    def __init__(self, _subNodes):
        self.subNodes = _subNodes
     
    class Iterator(object):
        def __init__(self, bb, node, *args, **kwargs):
            self.iterations = self._make_iterations(bb, node)

        def _make_iterations(self, bb, node):
            for c in node.subNodes:
                it = bb.new_iterator(c)
                while True:
                    x = it()
                    if x == RUNNING:
                        yield x
                    elif x == FAILURE:
                        yield x
                        return
                    else:
                        assert x == SUCCESS
                        break

            # all children are failed
            yield SUCCESS

        def __call__(self):
            return next(self.iterations)

class SelectNode(Node):
    def __init__(self, _subNodes):
        self.subNodes = _subNodes
    
    class Iterator(object):
        def __init__(self, bb, node):
            self.iterations = self._make_iterations(bb, node)

        def _make_iterations(self, bb, node):
            for c in node.subNodes:
                it = bb.new_iterator(c)
                while True:
                    x = it()
                    if x == RUNNING:
                        yield x
                    elif x == SUCCESS:
                        yield x
                        return
                    else:
                        assert x == FAILURE
                        break

            # all children are failed
            yield FAILURE

        def __call__(self):
            return next(self.iterations)

class Decorator(object):
    def __init__(self, decorators=None):
        self.decorators = decorators or []

    def __call__(self, node):
        assert isinstance(node, Node)
        return Decorated(self.decorators, node)
    def __mul__(self, other):
        if isinstance(other, Decorator):
            decorators = self.decorators[:]
            decorators.extend(other.decorators)
            return Decorator(decorators)
        elif isinstance(other, Node):
            node = other
            for deco in reversed(self.decorators):
                node = Decorated(deco, node)
            return node

class Decorated(Node):
    def __init__(self, decorator=None, node=None):
        self.decorator = decorator
        self.node = node

    class Iterator(object):
        def __init__(self, bb, node):
            self.decorator_instance = node.decorator(bb, node.node)

        def __call__(self):
            x = self.decorator_instance()
            if x is None:
                return SUCCESS
            assert x == SUCCESS or x == FAILURE or x == RUNNING
            return x


def blackboard(self, *args, **kwargs):
    return Blackboard(self, *args, **kwargs)

def action(func):
    return ActionNode(func)

def actionWithProps(func, *args, **kwargs):
    return ActionNode(partial(func, *args, *kwargs))


def condition(func):
    return ConditionNode(func)


def conditionWithProps(func, *args, **kwargs):
    return ConditionNode(partial(func, *args, *kwargs))

def sequence(subNodes):
    return SequenceNode(subNodes)

def select(subNodes):
    return SelectNode(subNodes) 

def generator_decorator(f):
    def ctor(bb, node):
        g = f(bb, node)
        def iter_func():
            try:
                return next(g)
            except StopIteration:
                return SUCCESS
        return iter_func
    return ctor
def decorator(f):
    if inspect.isgeneratorfunction(f):
        f = wraps(f)(generator_decorator(f))
    return Decorator([f])

@decorator
def not_(bb, node):
    func = bb.new_iterator(node)
    x = func()
    while x == RUNNING:
        yield x
        x = func()
    yield FAILURE if x == SUCCESS else SUCCESS


@decorator
def failer(bb, node):
    func = bb.new_iterator(node)
    while func() == RUNNING:
        yield RUNNING
    yield FAILURE

def passVars(*args):
    @decorator
    def worker(bb, node):
            func = bb.new_iterator(node)
            while func(*args) == RUNNING:
                yield RUNNING
    return worker