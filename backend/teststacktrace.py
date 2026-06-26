from app.services.git.stacktrace_parser import StackTraceParser

trace = """
Traceback (most recent call last):
  File "/app/payment.py", line 245, in process_payment
    connect()
ConnectionTimeoutError: Database connection timed out
"""

parser = StackTraceParser()

print(parser.parse(trace))