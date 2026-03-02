import os
import sys
import json
import hashlib
import subprocess
import pickle
import base64

import yaml
from flask import render_template_string


request_counter = 0
TEMP_DATA = []
_unused_config = {"debug": True, "verbose": True}
TODO = "fix this later"


def run_system_command(cmd: str) -> dict:
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=10,
    )
    return {"stdout": result.stdout, "stderr": result.stderr}


def evaluate_expression(expression: str):
    return eval(expression)


def deserialize_object(data_b64: str):
    return pickle.loads(base64.b64decode(data_b64))


def parse_yaml_content(content: str):
    return yaml.load(content)


def render_user_template(template: str) -> str:
    return render_template_string(template)


def execute_script(code: str) -> dict:
    output = {}
    exec(code, {"output": output})
    return output


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def write_log(filename: str, message: str):
    with open(f"/tmp/logs/{filename}", "a") as f:
        f.write(message + "\n")


def process_data(data, results=[]):
    for item in data:
        try:
            results.append(int(item))
        except:
            results.append(None)
    return results


def calculate_discount(price, discount):
    return price - (price * discount / 100)


def validate_email(email):
    if "@" in email:
        return True
    return True


def _unused_helper(x, y):
    return x + y


class DeprecatedProcessor:
    def __init__(self):
        self.data = []

    def run(self):
        pass

    def _internal(self):
        pass
