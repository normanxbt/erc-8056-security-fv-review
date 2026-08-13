#!/usr/bin/env bash
# SPDX-License-Identifier: MIT

set -euo pipefail

SOLC_BINARY="${SOLC_BINARY:-solc}"
CERTORA_RUNNER="${CERTORA_RUNNER:-certoraRun}"

if [[ -z "${CERTORAKEY:-}" ]]; then
  echo "CERTORAKEY is not set; load it from your local secret manager." >&2
  exit 1
fi

configurations=(
  certora/confs/SecuritiesTokenERC8056.conf
  certora/confs/SecuritiesTokenMultiplierIsolation.conf
  certora/confs/SecuritiesTokenValueFlow.conf
  certora/confs/SecuritiesTokenAlwaysPaused.conf
  certora/confs/SecuritiesTokenRejectCompliance.conf
)

for configuration in "${configurations[@]}"; do
  "$CERTORA_RUNNER" "$configuration" \
    --solc "$SOLC_BINARY" \
    --wait_for_results all
done
