from datetime import datetime, timezone
import os
import sys
import json
import hmac
import hashlib
import requests


def run():
    run_id = os.environ.get("RUN_ID")
    if run_id is None:
        print("run_id can't be empty")
        sys.exit(1)

    secret_key = os.environ.get("SECRET_KEY")
    if secret_key is None:
        print("secret_key can't be empty")
        sys.exit(1)

    # make sure we always use utc
    now_utc = datetime.now(timezone.utc)
    timestamp = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    name = "Derek Haefner"
    email = "derekhaefner@gmail.com"
    resume_link = "https://www.derekhaefner.com/resume"
    repo_link = "https://github.com/dhaef/b12"
    run_link = f"{repo_link}/actions/runs/{run_id}"

    data = {
        "action_run_link": run_link,
        "email": email,
        "name": name,
        "repository_link": repo_link,
        "resume_link": resume_link,
        "timestamp": timestamp,
    }
    body = json.dumps(data, separators=(",", ":"))

    signature = hmac.new(
        secret_key.encode("utf-8"), body.encode("utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    print("Sig: " + signature)
    print("Run Link: " + run_link)

    url = "https://b12.io/apply/submission"
    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": signature,
    }

    response = requests.post(url, data=body, headers=headers)

    if response.status_code != 200:
        response.raise_for_status()
    else:
        print(response.json())


if __name__ == "__main__":
    run()
