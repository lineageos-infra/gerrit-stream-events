Run arbitrary python code from gerrit stream events
---


usage: `ssh review gerrit stream-events | python main.py`

config includes an event type, filter, and a list of callable python functions that will be called if the filter matches. Functions will always be called with the raw event dict as the first argument to the function. 
```yaml
- name: www-buildkite
  type: ref-updated
  filter:
    refUpdate.project: LineageOS/android_packages_apps_DeskClock
  callables:
    test.TestFunc:
      name: www-preview
```

Example test.py:

```python
def TestFunc(event, name) -> None:
    print(event, name)
```