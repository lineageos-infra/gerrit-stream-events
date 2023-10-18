import fileinput
import importlib
import operator
import traceback

from functools import reduce
from typing import Any

import json
import yaml



class Config:
    name: str
    filter: dict[str, Any]
    callables: dict[str, dict[str, Any]]

    def __init__(self, name, filter, callables, **kwargs):
        self.name = name
        self.filter = filter
        self.callables = callables

    def __repr__(self):
        return f"{self.name} {self.filter} {self.callables}"

def find(element, data):
    keys = element.split(".")
    rv = data
    for key in keys:
        if key in rv:
            rv = rv[key]
        else:
            return
    return rv

def parse(configs: dict[str, list[Config]], event: dict) -> None:
    event_type = event.get("type", "")
    for conf in configs.get(event_type, []):
        if conf.filter:
            for k, v in conf.filter.items():
                if find(k, event) != v:
                    return

        if conf.callables:
            for k, v in conf.callables.items():
                module = ".".join(k.split(".")[:-1])
                function = k.split(".")[-1]
                mod = importlib.import_module(module)
                try:
                    getattr(mod, function)(event, **v)
                except Exception as e:
                    print(traceback.format_exc())


if __name__ == "__main__":    
    configs: dict[str, list[Config]] = {}
    with open("config.yaml", "r") as f:
        conf = yaml.load(f, yaml.Loader)
        for c in conf:
            configs.setdefault(c.get("type"), []).append(Config(**c))


    for line in fileinput.input():
        print(line)
        event = json.loads(line)
        parse(configs, event)



