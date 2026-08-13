# Source and license notice

This review package contains a mixed-license source snapshot. The SPDX identifiers embedded in individual files are authoritative for those files.

- `src/SecuritiesToken.sol` and some implementation-specific support files are marked `BUSL-1.1`.
- the ERC-8056 base/interfaces, verification harnesses/specifications, review tests, and scripts are marked `MIT` where indicated;
- files under `lib/` are the minimal OpenZeppelin compiler dependencies and retain their upstream notices and SPDX identifiers; and
- the prose documentation is provided as part of this research contribution and does not relicense the source snapshot.

Reference license texts are included under `LICENSES/`. No single top-level license is applied because the repository contains files under different terms.

`LICENSES/MIT-ZeroDrift.txt` applies only to the original verification specifications, harnesses, tests, and scripts contributed in this repository. It does not relicense the supplied ERC-8056 implementation snapshot or the OpenZeppelin dependencies, which retain their own file-level notices.

The supplied snapshot did not identify an upstream repository or include licensor-specific BUSL metadata beyond the file-level SPDX identifiers. This repository therefore does not guess an upstream provenance, licensor, Additional Use Grant, Change Date, or Change License. It republishes the reviewed files as received for non-production security research and reproducibility; users remain responsible for complying with the applicable file-level terms.

OpenZeppelin files under `lib/` are from the 5.3.0 release line and retain the OpenZeppelin copyright and MIT terms reproduced in `LICENSES/MIT-OpenZeppelin.txt`.
