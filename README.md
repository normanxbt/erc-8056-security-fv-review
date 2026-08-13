# ERC-8056 Security and Formal-Verification Contribution

This repository is a reproducible, implementation-scoped security contribution for the draft [ERC-8056 specification](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-8056.md).

It evaluates a pinned `SecuritiesToken` implementation with:

- Certora rules for access control, raw-accounting isolation, policy enforcement, value flow, interface support, and UI-view consistency;
- a concrete Foundry access-control regression test; and
- deterministic Foundry property-based tests for conversions and multiplier activation.

This is a public research artifact. A focused [Draft specification PR](https://github.com/ethereum/ERCs/pull/1944) has been submitted to `ethereum/ERCs`. The Ethereum Magicians contribution is prepared in this repository and is pending publication.

## Review map

- [Scope and assurance boundary](SCOPE.md)
- [Reproduction instructions](REPRODUCE.md)
- [Recorded results](RESULTS.md)
- [Ethereum Magicians draft](FORUM_DRAFT.md)
- [Pinned source hashes](SOURCE_SNAPSHOT.md)
- [Source and license notice](NOTICE.md)
- [Certora specifications](certora/specs)
- [Certora configurations](certora/confs)
- [Foundry tests](test/ERC8056SecurityProperties.t.sol)

## Verified property groups

For the pinned implementation and the assumptions encoded in each configuration:

1. a caller with neither the administrator nor issuer role cannot mint, burn, or call the implementation's multiplier scheduler;
2. scheduling a UI multiplier does not modify raw balances, raw total supply, or allowances;
3. a valid authorized scheduling call exposes the requested pending multiplier and effective timestamp;
4. successful ERC-20 value-moving operations have exact raw-accounting deltas under the linked policy model;
5. an always-paused or always-rejecting policy model blocks all tested value-moving entry points; and
6. the declared UI balance and total-supply views agree with the implementation's conversion function.

The Foundry suite separately exercises conversion formulae, monotonicity, floor-rounding behavior, raw-to-UI-to-raw non-creation, UI-view delegation, and raw-accounting preservation across scheduling and activation.

## Quick local check

```bash
./scripts/check-local.sh
```

Cloud verification requires the caller's own Certora credentials:

```bash
./scripts/run-certora.sh
```

## Publication sequence

1. Publish this reproducible repository.
2. Open a focused Draft specification PR.
3. Post the security/FV contribution to the ERC-8056 discussion and link the Draft PR.
4. Collect author feedback and revise the normative wording as needed.
