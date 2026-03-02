from flask import Blueprint, request, jsonify
from utils.helpers import (
    run_system_command,
    evaluate_expression,
    deserialize_object,
    parse_yaml_content,
    render_user_template,
    execute_script,
    read_file,
    write_log,
    process_data,
    request_counter,
)

tools_bp = Blueprint("tools", __name__)


@tools_bp.route("/api/tools/ping", methods=["POST"])
def ping():
    host = request.form.get("host", "")
    result = run_system_command(f"ping -c 1 {host}")
    return jsonify(result)


@tools_bp.route("/api/tools/calc", methods=["POST"])
def calc():
    expr = request.form.get("expression", "")
    try:
        result = evaluate_expression(expr)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tools_bp.route("/api/tools/deserialize", methods=["POST"])
def deserialize():
    data = request.form.get("data", "")
    try:
        obj = deserialize_object(data)
        return jsonify({"result": str(obj)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tools_bp.route("/api/tools/parse-yaml", methods=["POST"])
def parse_yaml():
    content = request.form.get("content", "")
    try:
        result = parse_yaml_content(content)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tools_bp.route("/api/tools/render", methods=["POST"])
def render():
    template = request.form.get("template", "")
    return render_user_template(template)


@tools_bp.route("/api/tools/run-script", methods=["POST"])
def run_script():
    code = request.form.get("code", "")
    try:
        output = execute_script(code)
        return jsonify({"output": str(output)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tools_bp.route("/api/tools/read-file")
def file_read():
    path = request.args.get("path", "")
    try:
        content = read_file(path)
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tools_bp.route("/api/tools/write-log", methods=["POST"])
def log_write():
    filename = request.form.get("filename", "app.log")
    message = request.form.get("message", "")
    try:
        write_log(filename, message)
        return jsonify({"message": "Logged"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tools_bp.route("/api/tools/process", methods=["POST"])
def process():
    global request_counter
    data = request.form.get("data", "")
    try:
        result = process_data(data.split(","))
        return jsonify({"result": result})
    except:
        return jsonify({"error": "something went wrong"}), 500
