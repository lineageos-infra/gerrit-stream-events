import fileinput
import importlib
import operator

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

def parse(configs: dict[str, list[Config]], data: dict) -> None:
    event_type = data.get("type", "")
    for conf in configs.get(event_type, []):
        if conf.filter:
            for k, v in conf.filter.items():
                if find(k, data) != v:
                    return

        if conf.callables:
            for k, v in conf.callables.items():
                module = ".".join(k.split(".")[:-1])
                function = k.split(".")[-1]
                mod = importlib.import_module(module)
                getattr(mod, function)(data, **v)

if __name__ == "__main__":    
    configs: dict[str, list[Config]] = {}
    with open("config.yaml", "r") as f:
        conf = yaml.load(f, yaml.Loader)
        for c in conf:
            configs.setdefault(c.get("type"), []).append(Config(**c))


    data = json.loads('{"submitter":{"name":"","email":"","username":""},"refUpdate":{"oldRev":"ab635e76af5eca50e4835aadefb8d183eb7960e9","newRev":"fe003da0cd8b6932651bc7f5e5573c6c0446fb76","refName":"refs/changes/41/367141/meta","project":"LineageOS/android_packages_apps_DeskClock"},"type":"ref-updated","eventCreatedOn":1696973217}')
    parse(configs, data)
    # for line in fileinput.input():
    #     #print(line)
    #     data = json.loads(line)
    #     parse(configs, data)



