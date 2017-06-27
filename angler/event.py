import inspect
import re


class Event(object):
    def __init__(self, event: str, result: list, invoke):
        self.event = re.compile(event)
        self.result = result
        self.invoke = invoke


def event_package_factory(package, params):
    mod = __import__(package, fromlist=[''])
    param_list = []
    for name in inspect.signature(mod.factory).parameters.keys():
        value = params.get(name)
        if value is not None:
            param_list.append(value)
        else:
            break
    data = mod.factory(*param_list)
    result = data.get('result')
    if result is None:
        result = []
    event = data.get('event')
    if event is None:
        event = params.get('event')
    return Event(event, result, data['invoke'])


def event_script_factory(event, result, script):
    def create_function():
        g = {}
        exec(script, g)
        for key in g.keys():
            if key != '__builtins__':
                return g[key]
        return None

    return Event(event, result, create_function())


def event_factory(node):
    event = node.get('event')
    result = node.get('result')
    script = node.get('script')
    package = node.get('package')
    if script is not None:
        return event_script_factory(event, result, script)
    else:
        return event_package_factory(package, node)
