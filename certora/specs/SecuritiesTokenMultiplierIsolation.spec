// SPDX-License-Identifier: MIT

methods {
    function setUIMultiplier(uint256,uint256) external;
    function balanceOf(address) external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;
    function allowance(address,address) external returns (uint256) envfree;

    function newUIMultiplier() external returns (uint256);
    function effectiveAt() external returns (uint256);
    function hasPendingMultiplier() external returns (bool);

    function DEFAULT_ADMIN_ROLE() external returns (bytes32) envfree;
    function ISSUER_ROLE() external returns (bytes32) envfree;
    function hasRole(bytes32,address) external returns (bool) envfree;
}

definition isAdminOrIssuer(address account) returns bool =
    hasRole(DEFAULT_ADMIN_ROLE(), account) || hasRole(ISSUER_ROLE(), account);

// Scheduling is a UI-layer operation: whether it succeeds or reverts, it must
// not change raw balances, raw total supply, or ERC-20 allowances.
rule schedulingPreservesRawAccounting(
    env e, uint256 newMultiplier, uint256 timestamp,
    address account, address owner, address spender
) {
    uint256 balanceBefore = balanceOf(account);
    uint256 supplyBefore = totalSupply();
    uint256 allowanceBefore = allowance(owner, spender);

    setUIMultiplier@withrevert(e, newMultiplier, timestamp);

    assert balanceOf(account) == balanceBefore;
    assert totalSupply() == supplyBefore;
    assert allowance(owner, spender) == allowanceBefore;
}

// For an authorized caller and valid SecuritiesToken bounds, scheduling must
// succeed and expose exactly the requested pending state.
rule validAuthorizedScheduleEstablishesPendingState(
    env e, uint256 newMultiplier, uint256 timestamp
) {
    require e.block.timestamp < 2^128;
    require e.msg.value == 0;
    require isAdminOrIssuer(e.msg.sender);
    require newMultiplier >= 1000000000;
    require newMultiplier <= 1000000000000000000000000000;
    require timestamp > e.block.timestamp;
    require timestamp <= e.block.timestamp + 31536000;

    setUIMultiplier@withrevert(e, newMultiplier, timestamp);

    assert !lastReverted;
    assert hasPendingMultiplier(e);
    assert newUIMultiplier(e) == newMultiplier;
    assert effectiveAt(e) == timestamp;
}
