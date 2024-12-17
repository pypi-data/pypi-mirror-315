import os
from django.http import Http404, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from typing import Generator


def read_line(log_file_path: str, buffer_size: int = 1024) -> Generator[str, None, None]:
    """
    Generator that reads JSON log entries from a log file.
    The log entries are read in the order they appear in the file.
    """
    with open(log_file_path, "rb") as file:
        buffer = file.read(buffer_size)

        while buffer:
            log_lines = buffer.split(b"\n")
            for line in log_lines[:-1]:
                yield line.decode("utf-8")
            leftover_line = log_lines[-1]
            next_buffer = file.read(buffer_size)
            if not next_buffer:
                # yield the last line if it's the end of the file
                yield leftover_line.decode("utf-8")
                break

            buffer = leftover_line + next_buffer


def stream_logs(log_file_path: str) -> Generator[bytes, None, None]:
    """
    Stream logs from the specified log file. Each line is a string in JSON format.
    """
    if not os.path.exists(log_file_path):
        raise Http404("Log file not found")

    for line in read_line(log_file_path):
        try:
            log_entry = json.loads(line)
            yield f"{json.dumps(log_entry)}\n".encode("utf-8")
        except json.JSONDecodeError:
            # Even if the log entry is not in JSON format, we still want to stream it
            yield f"{line}\n".encode("utf-8")



@login_required()
def logs_view(request, service_name: str) -> StreamingHttpResponse:
    """
    A view that streams the logs for a given service.
    """
    logs_path = os.environ.get("LOGS_PATH", "/opt/groundlight/logs")
    log_file_path = os.path.join(logs_path, f"{service_name}.log")
    response = StreamingHttpResponse(
        streaming_content=stream_logs(log_file_path), content_type="text/plain"
    )
    return response
