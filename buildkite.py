import os
import requests

def start_pipeline(event: dict, name: str) -> None:
    # starting pipelines from patchset-created events
    # data.patchSet.ref is the ref we want to pass to buildkite
    patchset = event.get("patchSet", {})
    ref = patchset.get("ref", "")

    change = event.get("change", {})
    number = change.get("number")

    token = os.environ.get("BUILDKITE_TOKEN")
    if not token:
        print("no buildkite token")
        return

    if ref:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "commit": ref,
            "branch": "main",
            "env": {
                "CHANGE_NUMBER": number,
            },
        }
        requests.post(f"https://api.buildkite.com/v2/organizations/lineageos/pipelines/{name}/builds", headers=headers, json=data)
