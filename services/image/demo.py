from opentelemetry import trace


def do_something():
    print("printing current span")
    print(trace.get_current_span())
