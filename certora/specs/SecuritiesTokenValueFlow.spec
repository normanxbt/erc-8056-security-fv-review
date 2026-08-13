// SPDX-License-Identifier: MIT

methods {
    function transfer(address,uint256) external returns (bool);
    function transferFrom(address,address,uint256) external returns (bool);
    function approve(address,uint256) external returns (bool);
    function mint(uint256) external returns (bool);
    function burn(uint256) external returns (bool);

    function balanceOf(address) external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;
    function allowance(address,address) external returns (uint256) envfree;

    function uiMultiplier() external returns (uint256);
    function newUIMultiplier() external returns (uint256);
    function effectiveAt() external returns (uint256);
    function hasPendingMultiplier() external returns (bool);
}

rule successfulTransferHasExactRawDeltas(
    env e, address recipient, address unrelated, address allowanceSpender, uint256 amount
) {
    require e.msg.sender != 0;
    require recipient != 0;
    require e.msg.sender != recipient;
    require unrelated != e.msg.sender && unrelated != recipient;

    uint256 senderBefore = balanceOf(e.msg.sender);
    uint256 recipientBefore = balanceOf(recipient);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();
    uint256 allowanceBefore = allowance(e.msg.sender, allowanceSpender);
    uint256 multiplierBefore = uiMultiplier(e);
    uint256 nextMultiplierBefore = newUIMultiplier(e);
    uint256 effectiveAtBefore = effectiveAt(e);
    bool pendingBefore = hasPendingMultiplier(e);

    // Certora starts from arbitrary storage. Exclude arithmetic states that a
    // reachable ERC-20 state cannot produce but unchecked OZ updates can wrap.
    require senderBefore >= amount;
    require recipientBefore <=
        0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff - amount;

    transfer@withrevert(e, recipient, amount);
    bool reverted = lastReverted;
    require !reverted;

    assert balanceOf(e.msg.sender) == senderBefore - amount;
    assert balanceOf(recipient) == recipientBefore + amount;
    assert balanceOf(unrelated) == unrelatedBefore;
    assert totalSupply() == supplyBefore;
    assert allowance(e.msg.sender, allowanceSpender) == allowanceBefore;
    assert uiMultiplier(e) == multiplierBefore;
    assert newUIMultiplier(e) == nextMultiplierBefore;
    assert effectiveAt(e) == effectiveAtBefore;
    assert hasPendingMultiplier(e) == pendingBefore;
}

rule successfulTransferFromHasExactRawDeltasAndAllowance(
    env e, address owner, address recipient, address unrelated, uint256 amount
) {
    require e.msg.sender != 0;
    require owner != 0 && recipient != 0;
    require e.msg.sender != owner;
    require owner != recipient;
    require unrelated != owner && unrelated != recipient;

    uint256 ownerBefore = balanceOf(owner);
    uint256 recipientBefore = balanceOf(recipient);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();
    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 multiplierBefore = uiMultiplier(e);

    require ownerBefore >= amount;
    require recipientBefore <=
        0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff - amount;
    require allowanceBefore >= amount;

    transferFrom@withrevert(e, owner, recipient, amount);
    bool reverted = lastReverted;
    require !reverted;

    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert balanceOf(owner) == ownerBefore - amount;
    assert balanceOf(recipient) == recipientBefore + amount;
    assert balanceOf(unrelated) == unrelatedBefore;
    assert totalSupply() == supplyBefore;
    assert allowanceBefore == 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        => allowanceAfter == allowanceBefore;
    assert allowanceBefore < 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        => allowanceAfter == allowanceBefore - amount;
    assert uiMultiplier(e) == multiplierBefore;
}

rule successfulMintHasExactRawDeltas(env e, address unrelated, uint256 amount) {
    require e.msg.sender != 0;
    require unrelated != e.msg.sender;

    uint256 callerBefore = balanceOf(e.msg.sender);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();
    uint256 multiplierBefore = uiMultiplier(e);
    uint256 nextMultiplierBefore = newUIMultiplier(e);
    uint256 effectiveAtBefore = effectiveAt(e);

    require callerBefore <=
        0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff - amount;
    require supplyBefore <=
        0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff - amount;

    mint@withrevert(e, amount);
    bool reverted = lastReverted;
    require !reverted;

    assert balanceOf(e.msg.sender) == callerBefore + amount;
    assert balanceOf(unrelated) == unrelatedBefore;
    assert totalSupply() == supplyBefore + amount;
    assert uiMultiplier(e) == multiplierBefore;
    assert newUIMultiplier(e) == nextMultiplierBefore;
    assert effectiveAt(e) == effectiveAtBefore;
}

rule successfulBurnHasExactRawDeltas(env e, address unrelated, uint256 amount) {
    require e.msg.sender != 0;
    require unrelated != e.msg.sender;

    uint256 callerBefore = balanceOf(e.msg.sender);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();
    uint256 multiplierBefore = uiMultiplier(e);
    uint256 nextMultiplierBefore = newUIMultiplier(e);
    uint256 effectiveAtBefore = effectiveAt(e);

    require callerBefore >= amount;
    require supplyBefore >= amount;

    burn@withrevert(e, amount);
    bool reverted = lastReverted;
    require !reverted;

    assert balanceOf(e.msg.sender) == callerBefore - amount;
    assert balanceOf(unrelated) == unrelatedBefore;
    assert totalSupply() == supplyBefore - amount;
    assert uiMultiplier(e) == multiplierBefore;
    assert newUIMultiplier(e) == nextMultiplierBefore;
    assert effectiveAt(e) == effectiveAtBefore;
}

rule successfulApproveOnlyChangesSelectedAllowance(
    env e, address spender, address otherSpender, address unrelated, uint256 amount
) {
    require e.msg.sender != 0;
    require otherSpender != spender;

    uint256 balanceBefore = balanceOf(e.msg.sender);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();
    uint256 otherAllowanceBefore = allowance(e.msg.sender, otherSpender);
    uint256 multiplierBefore = uiMultiplier(e);

    approve@withrevert(e, spender, amount);
    bool reverted = lastReverted;
    require !reverted;

    assert allowance(e.msg.sender, spender) == amount;
    assert allowance(e.msg.sender, otherSpender) == otherAllowanceBefore;
    assert balanceOf(e.msg.sender) == balanceBefore;
    assert balanceOf(unrelated) == unrelatedBefore;
    assert totalSupply() == supplyBefore;
    assert uiMultiplier(e) == multiplierBefore;
}

rule revertedTransferRollsBackRawAccounting(env e, address recipient, address unrelated, uint256 amount) {
    uint256 senderBefore = balanceOf(e.msg.sender);
    uint256 recipientBefore = balanceOf(recipient);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();

    transfer@withrevert(e, recipient, amount);
    bool reverted = lastReverted;

    assert reverted => balanceOf(e.msg.sender) == senderBefore;
    assert reverted => balanceOf(recipient) == recipientBefore;
    assert reverted => balanceOf(unrelated) == unrelatedBefore;
    assert reverted => totalSupply() == supplyBefore;
}

rule revertedTransferFromRollsBackRawAccounting(
    env e, address owner, address recipient, address unrelated, uint256 amount
) {
    uint256 ownerBefore = balanceOf(owner);
    uint256 recipientBefore = balanceOf(recipient);
    uint256 unrelatedBefore = balanceOf(unrelated);
    uint256 supplyBefore = totalSupply();
    uint256 allowanceBefore = allowance(owner, e.msg.sender);

    transferFrom@withrevert(e, owner, recipient, amount);
    bool reverted = lastReverted;

    assert reverted => balanceOf(owner) == ownerBefore;
    assert reverted => balanceOf(recipient) == recipientBefore;
    assert reverted => balanceOf(unrelated) == unrelatedBefore;
    assert reverted => totalSupply() == supplyBefore;
    assert reverted => allowance(owner, e.msg.sender) == allowanceBefore;
}
