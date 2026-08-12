# The sandbox image for grading Node-based submissions (TypeScript, JavaScript).
#
# Same shape and same reasoning as runner.Dockerfile: an interpreter and nothing
# else. No npm packages, so there is no dependency tree to audit and a submission
# has nothing to import but the standard library.
#
# Node 22.6+ is required: below that, running a .mts file is a syntax error
# rather than type-stripping, which would look like the learner's mistake. The
# tag is pinned to a major so a rebuild cannot silently drop under that floor.
FROM node:22-alpine

# npm and corepack are removed. They are the only things in this image that talk
# to a network or execute downloaded code, and grading needs neither.
RUN rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx \
           /usr/local/bin/corepack /opt/yarn* 2>/dev/null || true

RUN mkdir -p /repo /runner /work && chown -R 65534:65534 /repo /runner /work

USER 65534:65534
WORKDIR /tmp

# No ENTRYPOINT: the executor passes the exact argv, so the sandbox flags and the
# command stay visible in one place.
