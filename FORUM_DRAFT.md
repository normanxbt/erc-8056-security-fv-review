# Draft Ethereum Magicians contribution

Proposed title: **Reproducible security and formal-verification properties for ERC-8056**

---

I prepared a reproducible, implementation-scoped security and formal-verification contribution for ERC-8056 against a pinned `SecuritiesToken` implementation.

Repository: [github.com/normanxbt/erc-8056-security-fv-review](https://github.com/normanxbt/erc-8056-security-fv-review)

The repository contains the pinned Solidity source, Certora specifications and configurations, deterministic Foundry property tests, exact reproduction commands, source hashes, and direct Prover reports.

For this implementation, the Certora suite establishes that:

- a caller with neither the administrator nor issuer role cannot mint, burn, or invoke the implementation's multiplier scheduler;
- scheduling a multiplier does not modify raw balances, raw total supply, or allowances;
- a valid authorized schedule exposes exactly the requested pending multiplier and effective timestamp;
- successful value-moving operations have exact raw-accounting deltas under the explicitly linked permissive policy model;
- the explicitly linked paused and rejecting policy models block the tested value-moving operations; and
- the declared UI balance and total-supply views agree with the implementation's conversion function.

The Foundry suite adds a fixed-seed, 1,000-run campaign for the conversion formula, monotonicity, floor-rounding behavior, raw-to-UI-to-raw non-creation, UI-view delegation, raw-accounting preservation across scheduling and activation, zero conversion, and an unprivileged-caller regression test.

The implementation has a scheduled two-argument updater and pending-state getters, so the updater-specific properties are implementation-scoped. The following property templates appear portable across ERC-8056 implementations:

1. accepting a UI-multiplier updater call must not mutate raw ERC-20 balances, raw total supply, or allowances;
2. UI balance and UI total-supply views must apply the same conversion semantics as the implementation's public conversion function;
3. any implementation-provided multiplier updater must machine-check its stated authorization policy; and
4. for an implementation with pending updates, a successful scheduling call must make its pending-state getters expose exactly the accepted multiplier and effective timestamp.

Would the authors be open to a focused follow-up specification PR that expresses these as security requirements or recommended machine-checkable invariants, while leaving updater mechanics implementation-defined?

Prover reports:

- [ERC-8056 core and interface properties](https://prover.certora.com/output/10277929/c7010e3290574d48931cdb622762060b)
- [Multiplier raw-accounting isolation and pending state](https://prover.certora.com/output/10277929/6b7f0222a55744d5b7095f9a20ae2777)
- [Raw value-flow properties](https://prover.certora.com/output/10277929/aca634da5b1d46fba00d988ad5c361bc)
- [Paused-policy enforcement](https://prover.certora.com/output/10277929/618d96ec5e0640fab8e37522045a655c)
- [Compliance-policy enforcement](https://prover.certora.com/output/10277929/ded1c6af61774d79bb6f35f7328aa70b)

---

Review note: draft only. Do not post until the repository contents and wording receive separate approval.
