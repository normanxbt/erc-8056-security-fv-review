# Scope and assurance boundary

## Target

The target is the source snapshot under `src/`. `SOURCE_SNAPSHOT.md` pins every target file with SHA-256 so another reviewer can confirm that the same implementation was evaluated.

The standards reference is the current draft [`ERCS/erc-8056.md`](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-8056.md).

The target implementation exposes a two-argument `setUIMultiplier(uint256,uint256)` scheduler and an additional `IERC8056Scheduled` interface. Those are implementation choices. Properties about scheduling authorization, time bounds, and pending-state getters are therefore implementation-scoped evidence, not claims that every ERC-8056 implementation must use this API.

## Certora model

The Certora suite is split into five configurations:

- `SecuritiesTokenERC8056.conf`: interface support, pending-state consistency, conversion/view consistency, role enforcement, and scheduling input guards;
- `SecuritiesTokenMultiplierIsolation.conf`: raw-accounting isolation and exact pending state after a valid authorized schedule;
- `SecuritiesTokenValueFlow.conf`: exact successful raw value flow with an always-unpaused, always-compliant linked policy model;
- `SecuritiesTokenAlwaysPaused.conf`: denial behavior with an always-paused linked policy model; and
- `SecuritiesTokenRejectCompliance.conf`: denial behavior with an always-rejecting linked compliance model.

The linked contracts in `certora/harness/PolicyManagers.sol` are explicit verification models, not production policy implementations.

Every rule's preconditions are part of the property. In particular, arithmetic bounds and policy-manager behavior must be read together with a rule's conclusion.

## Foundry model

The Foundry suite deploys the implementation behind a minimal delegate proxy so its initializer can run. It uses:

- one administrator: the test contract;
- one issuer: `0x000000000000000000000000000000000000bEEF`;
- one unprivileged address: `0x00000000000000000000000000000000000A11cE`;
- an always-compliant compliance model; and
- an always-unpaused pause model.

The fixed fuzz seed and run count make the recorded test campaign repeatable. These are property-based tests, not exhaustive proofs.

## Claim boundary

The recorded conclusions apply to the pinned implementation, the included rules, their stated preconditions, and the named linked models. They do not assert verification of the ERC text as a whole or of implementations not present in this repository.
