#!/usr/bin/env bash
#
# https://medium.com/@adrian.gheorghe.dev/using-docker-secrets-in-your-environment-variables-7a0609659aab
#

set -e

inject_env() {
  local variable="${1}"
  local secret_file=/run/secrets/"${variable}"
  local value="$(cat "${secret_file}")"
  export "${variable}"="${value}"
}


# Call the upstream entrypoint
exec gosu "${RUNTIME_UID_GID}" /usr/bin/tini -- "$@"
