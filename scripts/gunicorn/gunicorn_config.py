# Gunicorn configuration file: config.py

# Server socket
#
#   bind - The server socket to bind
#   backlog - The number of pending connections. This refers
#             to the number of clients that can be waiting to be
#             served. Exceeding this number results in the client
#             getting an error when attempting to connect. It should
#             only affect servers under significant load.
#
#   Useful if you want to control the socket backlog and tune it.
#   Must be a positive integer. Generally set in the 64-2048 range.
bind = '0.0.0.0:9000'
backlog = 2048

# Worker processes
#
#   workers - The number of worker processes that this server
#             should keep alive for handling requests.
#   worker_class - The type of workers to use. The default sync class
#                  should handle most 'normal' types of workloads.
#                  You'll want to read http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#                  for information on when you might want to choose
#                  one of the other worker classes.
#
#   An simple way to compute the number of workers is 2-4 x $(NUM_CORES).
#   You can check your machine's cores with `nproc` or by viewing proc info with `lscpu`.
workers = 3
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000

# Security
#
#   limit_request_line - The maximum size of HTTP request line in bytes.
#   limit_request_fields - Limit the number of HTTP headers fields in a request.
limit_request_line = 4094
limit_request_fields = 20

# Debugging
#
#   reload - Whether to restart workers when code changes. This should only
#            be used for development.
reload = False

# Logging
#
#   accesslog - The file to which Gunicorn will write access logs. If not set,
#               Gunicorn will send access logs to stdout.
#   errorlog - The file to which Gunicorn will write error logs. If not set,
#              Gunicorn will send error logs to stderr.
#   loglevel - The granularity of log output
# Define logging level
loglevel = "info"
# Enable access log and format
accesslog = "-"  # '-' means log to stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Proc Name
#
#   proc_name - A base to use with setproctitle for process naming.
#               This affects things like `ps` and `top`.
proc_name = 'django_chatbot_app'
