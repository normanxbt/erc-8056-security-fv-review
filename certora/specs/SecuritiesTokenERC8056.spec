// SPDX-License-Identifier: MIT

methods {
    function supportsInterface(bytes4) external returns (bool) envfree;

    function uiMultiplier() external returns (uint256);
    function newUIMultiplier() external returns (uint256);
    function effectiveAt() external returns (uint256);
    function hasPendingMultiplier() external returns (bool);
    function pendingMultiplier() external returns (uint256,uint256);

    function toUIAmount(uint256) external returns (uint256);
    function fromUIAmount(uint256) external returns (uint256);
    function balanceOf(address) external returns (uint256) envfree;
    function balanceOfUI(address) external returns (uint256);
    function totalSupply() external returns (uint256) envfree;
    function totalSupplyUI() external returns (uint256);

    function DEFAULT_ADMIN_ROLE() external returns (bytes32) envfree;
    function ISSUER_ROLE() external returns (bytes32) envfree;
    function hasRole(bytes32,address) external returns (bool) envfree;
}

definition multiplierWithinSecuritiesTokenBounds(env e) returns bool =
    uiMultiplier(e) >= 1000000000 &&
    uiMultiplier(e) <= 1000000000000000000000000000;

definition isNotAdminOrIssuer(address account) returns bool =
    !hasRole(DEFAULT_ADMIN_ROLE(), account) &&
    !hasRole(ISSUER_ROLE(), account);

rule supportsDeclaredErc8056Interfaces() {
    assert supportsInterface(to_bytes4(0xa60bf13d)); // IScaledUIAmount
    assert supportsInterface(to_bytes4(0x4bd27648)); // IScaledUIAmountNewUIMultiplier
    assert supportsInterface(to_bytes4(0x57854fc3)); // IScaledUIAmountConversion
    assert supportsInterface(to_bytes4(0xd890fd71)); // IScaledUIAmountBalances
    assert supportsInterface(to_bytes4(0xeb0093dd)); // IERC8056Scheduled extension
}

rule noPendingMultiplierSentinel(env e) {
    bool pending = hasPendingMultiplier(e);
    uint256 multiplier;
    uint256 timestamp;

    multiplier, timestamp = pendingMultiplier(e);

    assert !pending => multiplier == 0 && timestamp == 0;
    assert pending => timestamp > 0;
}

rule noPendingEffectiveAtZero(env e) {
    bool pending = hasPendingMultiplier(e);
    uint256 timestamp = effectiveAt(e);

    assert !pending => timestamp == 0;
    assert pending => timestamp > 0;
}

rule newMultiplierEqualsCurrentWhenNoPending(env e) {
    require !hasPendingMultiplier(e);

    assert newUIMultiplier(e) == uiMultiplier(e);
}

rule zeroConversionIsZeroWhenMultiplierInitialized(env e) {
    require multiplierWithinSecuritiesTokenBounds(e);

    assert toUIAmount(e, 0) == 0;
    assert fromUIAmount(e, 0) == 0;
}

rule uiBalanceMatchesConversion(env e, address account) {
    require multiplierWithinSecuritiesTokenBounds(e);
    require balanceOf(account) < 2^128;
    require uiMultiplier(e) < 2^128;

    assert balanceOfUI(e, account) == toUIAmount(e, balanceOf(account));
}

rule totalSupplyUiMatchesConversion(env e) {
    require multiplierWithinSecuritiesTokenBounds(e);
    require totalSupply() < 2^128;
    require uiMultiplier(e) < 2^128;

    assert totalSupplyUI(e) == toUIAmount(e, totalSupply());
}

rule unauthorizedCannotMint(env e, uint256 amount) {
    require e.msg.sender != 0;
    require isNotAdminOrIssuer(e.msg.sender);

    mint@withrevert(e, amount);

    assert lastReverted;
}

rule unauthorizedCannotBurn(env e, uint256 amount) {
    require e.msg.sender != 0;
    require isNotAdminOrIssuer(e.msg.sender);

    burn@withrevert(e, amount);

    assert lastReverted;
}

rule unauthorizedCannotScheduleMultiplier(env e, uint256 newMultiplier, uint256 timestamp) {
    require e.msg.sender != 0;
    require isNotAdminOrIssuer(e.msg.sender);

    setUIMultiplier@withrevert(e, newMultiplier, timestamp);

    assert lastReverted;
}

rule multiplierScheduleInputGuards(env e, uint256 newMultiplier, uint256 timestamp) {
    require e.block.timestamp < 2^128;
    require hasRole(DEFAULT_ADMIN_ROLE(), e.msg.sender) || hasRole(ISSUER_ROLE(), e.msg.sender);

    setUIMultiplier@withrevert(e, newMultiplier, timestamp);

    assert newMultiplier < 1000000000 => lastReverted;
    assert newMultiplier > 1000000000000000000000000000 => lastReverted;
    assert timestamp <= e.block.timestamp => lastReverted;
    assert timestamp > e.block.timestamp + 31536000 => lastReverted;
}
