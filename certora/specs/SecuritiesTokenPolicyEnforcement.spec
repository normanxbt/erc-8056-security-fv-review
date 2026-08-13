// SPDX-License-Identifier: MIT

methods {
    function transfer(address,uint256) external returns (bool);
    function transferFrom(address,address,uint256) external returns (bool);
    function mint(uint256) external returns (bool);
    function burn(uint256) external returns (bool);
}

// This spec is run twice: once with an always-paused pause manager and once
// with an always-rejecting compliance manager. In either environment no raw
// value-moving operation may complete.
rule policyDenialBlocksAllValueMovingEntryPoints(
    env e, address owner, address recipient, uint256 amount
) {
    transfer@withrevert(e, recipient, amount);
    bool transferReverted = lastReverted;
    transferFrom@withrevert(e, owner, recipient, amount);
    bool transferFromReverted = lastReverted;
    mint@withrevert(e, amount);
    bool mintReverted = lastReverted;
    burn@withrevert(e, amount);
    bool burnReverted = lastReverted;

    assert transferReverted;
    assert transferFromReverted;
    assert mintReverted;
    assert burnReverted;
}
