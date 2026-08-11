# The sandbox image for grading submissions.
#
# Deliberately almost empty. It contains a Python interpreter and nothing else:
# no pip, no shell utilities worth having, no package index credentials, no
# network tools. The curriculum and the runner script are bind-mounted read-only
# at run time, so this image does not need rebuilding when a problem changes.
#
# alpine keeps it small (~50 MB), and the submitted code only ever uses the
# standard library -- the reference specs import math, itertools, heapq and
# collections, all of which are built in.
FROM python:3.12-alpine

# Nothing is installed, so there is nothing to keep up to date except the base
# image itself. Rebuild periodically to pick up interpreter security fixes.

# A non-root user exists in the image so `--user 65534:65534` maps to a real
# entry; the container is also started read-only, so this is belt and braces.
RUN mkdir -p /repo /runner && chown -R 65534:65534 /repo /runner

# Compiling the stdlib to .pyc at build time means a read-only container with
# PYTHONDONTWRITEBYTECODE does not pay compilation cost on every submission.
RUN python -m compileall -q /usr/local/lib/python3.12 || true

USER 65534:65534
WORKDIR /tmp

# No ENTRYPOINT: the executor passes the exact argv, which keeps the sandbox
# flags and the command visible in one place rather than split across two.
