# Recorded results

Recorded on 2026-08-13 against the hashes in `SOURCE_SNAPSHOT.md`.

## Certora Prover

All 22 rule executions in the five selected configurations completed successfully. The suite contains 21 distinct named rules; the policy-denial rule is executed once with the paused model and once with the rejecting-compliance model.

| Configuration | Rules | Result | Prover report |
|---|---:|---|---|
| `SecuritiesTokenERC8056.conf` | 11 | Passed | [report](https://prover.certora.com/output/10277929/c7010e3290574d48931cdb622762060b) |
| `SecuritiesTokenMultiplierIsolation.conf` | 2 | Passed | [report](https://prover.certora.com/output/10277929/6b7f0222a55744d5b7095f9a20ae2777) |
| `SecuritiesTokenValueFlow.conf` | 7 | Passed | [report](https://prover.certora.com/output/10277929/aca634da5b1d46fba00d988ad5c361bc) |
| `SecuritiesTokenAlwaysPaused.conf` | 1 | Passed | [report](https://prover.certora.com/output/10277929/618d96ec5e0640fab8e37522045a655c) |
| `SecuritiesTokenRejectCompliance.conf` | 1 | Passed | [report](https://prover.certora.com/output/10277929/ded1c6af61774d79bb6f35f7328aa70b) |

For the pinned implementation and the assumptions encoded in the rules, the reports establish:

- callers without the administrator or issuer role cannot reach the tested mint, burn, or multiplier-scheduling entry points;
- multiplier scheduling preserves raw balances, raw total supply, and allowances;
- a valid authorized schedule establishes the requested pending multiplier and effective timestamp;
- successful transfers, delegated transfers, minting, and burning have the stated exact raw-accounting deltas under the named permissive policy model;
- the named denying policy models block the tested value-moving operations; and
- the implementation's declared ERC-8056 interfaces, conversion paths, UI balance view, and UI total-supply view satisfy the included consistency rules.

The scheduling API and its pending-state rules are specific to this implementation. Raw-accounting isolation and agreement between UI views and the conversion function are suitable reusable property templates for other ERC-8056 implementations.

## Foundry

The fixed-seed campaign completed with 8 passing tests and 0 failures.

The captured console output is available at [`results/foundry-20260813.txt`](results/foundry-20260813.txt).

| Test | Runs | Result |
|---|---:|---|
| `testFuzz_ConversionMatchesFloorFormula` | 1,000 | Passed |
| `testFuzz_ConversionsAreMonotonic` | 1,000 | Passed |
| `testFuzz_MultiplierSchedulingAndActivationPreserveRawAccounting` | 1,000 | Passed |
| `testFuzz_RawToUIToRawNeverCreatesRawAmount` | 1,000 | Passed |
| `testFuzz_ToUIFloorAdditivity` | 1,000 | Passed |
| `testFuzz_UIViewsDelegateToConversion` | 1,000 | Passed |
| `test_UnprivilegedCallerCannotReachPrivilegedEntryPoints` | 1 | Passed |
| `test_ZeroConversionsAreZero` | 1 | Passed |

These deterministic property-based tests provide reproducible regression coverage; the Certora rules above are the formal-verification claims.
