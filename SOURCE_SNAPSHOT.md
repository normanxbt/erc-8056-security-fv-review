# Pinned source snapshot

These SHA-256 values identify the implementation and local verification harness evaluated in the recorded run. Recompute them from the repository root with:

```bash
find src certora/harness test -type f -print0 | sort -z | xargs -0 shasum -a 256
```

| SHA-256 | File |
|---|---|
| `3694a87239863e9edc438b33a845ed4dbe61aaadff28814688fc1a359dd5f2c2` | `src/SecuritiesToken.sol` |
| `61b08f6653e4e9bd1ca2ad49162837cafa9618451eddcff5c78248daea632587` | `src/scaledUIToken/ERC8056/ERC8056BaseUpgradeable.sol` |
| `bb2b7f5a54f78fc87a7be71064ae1812acded89cce46a513233ea8b85005f47e` | `src/scaledUIToken/ERC8056/IERC8056Scheduled.sol` |
| `53a6b3449faa0138444888696d7f44f44e1415d7703e9f9dcbb4a06e30fa269c` | `src/scaledUIToken/ERC8056/IScaledUIAmount.sol` |
| `75d567f3d3068aaec2a1a91dc7c6c7cc39ba30004101d3964fd192b9939683b8` | `src/scaledUIToken/ERC8056/IScaledUIAmountBalances.sol` |
| `bb2351ae75c3c200a7a3783e26a159c7459feee76fe57a61729ebfa9c5f521da` | `src/scaledUIToken/ERC8056/IScaledUIAmountConversion.sol` |
| `11397ea2d7a2b6bd43e8be31db94b214bf3e83626c174de0e8b735490b4fef6e` | `src/scaledUIToken/ERC8056/IScaledUIAmountNewUIMultiplier.sol` |
| `ba22d7e1879799944db1e1b473e49b0f790d0aa608fa1978ce160a03b6f09117` | `src/scaledUIToken/compliance/ComplianceClientUpgradeable.sol` |
| `c937e0871d8fc748cb2fcb8d8047259e2b28b9b1f5e120e68c8dfe69fb42d04d` | `src/scaledUIToken/compliance/ICompliance.sol` |
| `74cbdc4faff69f4643d1abfeff9859b2baa1a9229822f9b91253af7a2841a8a5` | `src/scaledUIToken/pauseManager/IPauseManager.sol` |
| `979e5fb3f99f6c8be1027f44420fc0873187a4d4b8440591d88d2b660456fb1d` | `src/scaledUIToken/pauseManager/PauseManagerClientUpgradeable.sol` |
| `80073aae5119bac2d4a462c4df013b8b18a00a581a9c0ab506207e52e0709a94` | `certora/harness/PolicyManagers.sol` |
| `09365a44162235cc3d14e4a0e3db0f12cc421ce2afc34188521884f39a89c682` | `test/ERC8056SecurityProperties.t.sol` |

The files under `lib/` are the minimal compiler dependencies copied with the snapshot. Their embedded SPDX identifiers and notices remain authoritative.

This package records the source snapshot supplied for review, not a claim about its upstream repository or deployment. File-level SPDX identifiers and the accompanying `NOTICE.md` and `LICENSES/` materials define the publication boundary used here.

## Verification inputs

These hashes pin the specifications and configurations associated with the recorded reports:

| SHA-256 | File |
|---|---|
| `33c8a6e7b91915784fe8ab91e7857279d34da3709323dc5c41c794a99fa31b14` | `certora/specs/SecuritiesTokenERC8056.spec` |
| `3f7209ab37e6566a06012e451b12b842933ae398cb3d6e1c11185a4440c3fc66` | `certora/specs/SecuritiesTokenMultiplierIsolation.spec` |
| `bf3c4c3a2c0803f1dee8266a9aa9d565ecbb45622db09783daedddad8f65145f` | `certora/specs/SecuritiesTokenPolicyEnforcement.spec` |
| `e0284f325470fd4ee055cae40f2efd7df25a0aeea0c09175bd572e5eda460973` | `certora/specs/SecuritiesTokenValueFlow.spec` |
| `047cc8ed219d427dc8ad15a4da3f8bed6fdbefd442b6eda8aa53066469f9b30f` | `certora/confs/SecuritiesTokenAlwaysPaused.conf` |
| `23c57328352406ad6344353075ba776cfd08e4f2ce521fbd5c7e20d58db2a8f3` | `certora/confs/SecuritiesTokenERC8056.conf` |
| `22e546da6e8afe55f50ce964129eb89e36e372c704860f5a533d59e8625b45e0` | `certora/confs/SecuritiesTokenMultiplierIsolation.conf` |
| `1930abfdb4fc58d123e1f1117416a0dce113fcaa6ec4b826adf7539de5fdd646` | `certora/confs/SecuritiesTokenRejectCompliance.conf` |
| `ccae5a34dae5dc63ac91acdaad3cd30747f1344fb8a3aa56504cb0aa97c3ba62` | `certora/confs/SecuritiesTokenValueFlow.conf` |
