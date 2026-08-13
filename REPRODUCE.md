# Reproduction

The recorded run used:

- Forge `1.6.0-v1.7.0` (`f83bad6`);
- Solidity `0.8.29`; and
- `certora-cli` `8.18.0`.

Run all local checks from the repository root:

```bash
SOLC_BINARY=/absolute/path/to/solc \
CERTORA_RUNNER=/absolute/path/to/certoraRun \
./scripts/check-local.sh
```

This runs the deterministic Foundry campaign and performs a complete Certora compilation pass for each selected configuration.

To submit the same five configurations to Certora Prover, provide the credential through the Certora-supported `CERTORAKEY` environment variable and run:

```bash
SOLC_BINARY=/absolute/path/to/solc \
CERTORA_RUNNER=/absolute/path/to/certoraRun \
./scripts/run-certora.sh
```

The scripts never contain a credential value. Use a local secret manager or an ephemeral shell environment and do not commit keys, command histories containing keys, or generated Certora internals.

## Direct commands

Foundry:

```bash
forge test \
  --use /absolute/path/to/solc \
  -vv \
  --fuzz-runs 1000 \
  --fuzz-seed 0x8056
```

Certora compilation-only check:

```bash
certoraRun certora/confs/SecuritiesTokenERC8056.conf \
  --solc /absolute/path/to/solc \
  --compilation_steps_only
```

Certora cloud submission:

```bash
certoraRun certora/confs/SecuritiesTokenERC8056.conf \
  --solc /absolute/path/to/solc \
  --wait_for_results all
```

Repeat the Certora command for the configuration files listed in `scripts/run-certora.sh`.
