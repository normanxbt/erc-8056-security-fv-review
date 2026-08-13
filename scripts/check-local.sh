#!/usr/bin/env bash
# SPDX-License-Identifier: MIT

set -euo pipefail

SOLC_BINARY="${SOLC_BINARY:-solc}"
CERTORA_RUNNER="${CERTORA_RUNNER:-certoraRun}"

configurations=(
  certora/confs/SecuritiesTokenERC8056.conf
  certora/confs/SecuritiesTokenMultiplierIsolation.conf
  certora/confs/SecuritiesTokenValueFlow.conf
  certora/confs/SecuritiesTokenAlwaysPaused.conf
  certora/confs/SecuritiesTokenRejectCompliance.conf
)

forge test \
  --use "$SOLC_BINARY" \
  -vv \
  --fuzz-runs 1000 \
  --fuzz-seed 0x8056

for configuration in "${configurations[@]}"; do
  "$CERTORA_RUNNER" "$configuration" \
    --solc "$SOLC_BINARY" \
    --compilation_steps_only
done
