// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {SecuritiesToken} from "src/SecuritiesToken.sol";
import {
    AlwaysCompliantCompliance,
    AlwaysUnpausedPauseManager
} from "certora/harness/PolicyManagers.sol";

interface Vm {
    function prank(address sender) external;
    function warp(uint256 timestamp) external;
}

/// Minimal delegate proxy used only to exercise the implementation's initializer.
contract TestERC1967Proxy {
    bytes32 private constant IMPLEMENTATION_SLOT =
        bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);

    constructor(address implementation, bytes memory initializationCall) payable {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            sstore(slot, implementation)
        }

        (bool ok, bytes memory returnData) = implementation.delegatecall(initializationCall);
        if (!ok) {
            assembly {
                revert(add(returnData, 0x20), mload(returnData))
            }
        }
    }

    fallback() external payable {
        _delegate();
    }

    receive() external payable {
        _delegate();
    }

    function _delegate() private {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            let implementation := sload(slot)
            calldatacopy(0, 0, calldatasize())
            let success := delegatecall(gas(), implementation, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch success
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}

contract ERC8056SecurityPropertiesTest {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    uint256 private constant MULTIPLIER_SCALE = 1e18;
    uint256 private constant MIN_MULTIPLIER = 1e9;
    uint256 private constant MAX_MULTIPLIER = 1e27;

    address private constant ISSUER = address(0xBEEF);
    address private constant UNPRIVILEGED = address(0xA11CE);

    SecuritiesToken private token;

    function setUp() public {
        AlwaysCompliantCompliance compliance = new AlwaysCompliantCompliance();
        AlwaysUnpausedPauseManager pauseManager = new AlwaysUnpausedPauseManager();
        SecuritiesToken implementation = new SecuritiesToken();

        address[] memory issuers = new address[](1);
        issuers[0] = ISSUER;

        bytes memory initializationCall = abi.encodeCall(
            SecuritiesToken.initialize,
            (
                "ERC-8056 Review Token",
                "E8056",
                "REVIEW-8056",
                address(compliance),
                address(pauseManager),
                address(this),
                issuers
            )
        );

        TestERC1967Proxy proxy = new TestERC1967Proxy(address(implementation), initializationCall);
        token = SecuritiesToken(address(proxy));
    }

    /// Concrete negative-control PoC: an address with neither role cannot mint,
    /// burn, or schedule a multiplier, and all observed state remains unchanged.
    function test_UnprivilegedCallerCannotReachPrivilegedEntryPoints() public {
        uint256 supplyBefore = token.totalSupply();
        uint256 balanceBefore = token.balanceOf(UNPRIVILEGED);
        uint256 multiplierBefore = token.uiMultiplier();
        bool pendingBefore = token.hasPendingMultiplier();

        vm.prank(UNPRIVILEGED);
        (bool mintOk, bytes memory mintReturn) =
            address(token).call(abi.encodeCall(SecuritiesToken.mint, (1 ether)));

        vm.prank(UNPRIVILEGED);
        (bool burnOk, bytes memory burnReturn) =
            address(token).call(abi.encodeCall(SecuritiesToken.burn, (1 ether)));

        vm.prank(UNPRIVILEGED);
        (bool scheduleOk, bytes memory scheduleReturn) = address(token).call(
            abi.encodeWithSignature(
                "setUIMultiplier(uint256,uint256)", 2e18, block.timestamp + 1 days
            )
        );

        require(!mintOk && _selector(mintReturn) == SecuritiesToken.UnauthorizedRole.selector);
        require(!burnOk && _selector(burnReturn) == SecuritiesToken.UnauthorizedRole.selector);
        require(
            !scheduleOk
                && _selector(scheduleReturn) == SecuritiesToken.UnauthorizedRole.selector
        );
        require(token.totalSupply() == supplyBefore);
        require(token.balanceOf(UNPRIVILEGED) == balanceBefore);
        require(token.uiMultiplier() == multiplierBefore);
        require(token.hasPendingMultiplier() == pendingBefore);
    }

    function testFuzz_ConversionMatchesFloorFormula(uint128 rawAmount, uint128 uiAmount, uint256 seed)
        public
    {
        uint256 multiplier = _activateBoundedMultiplier(seed);

        uint256 expectedUI = uint256(rawAmount) * multiplier / MULTIPLIER_SCALE;
        uint256 expectedRaw = uint256(uiAmount) * MULTIPLIER_SCALE / multiplier;

        require(token.toUIAmount(rawAmount) == expectedUI);
        require(token.fromUIAmount(uiAmount) == expectedRaw);
    }

    function testFuzz_RawToUIToRawNeverCreatesRawAmount(uint128 rawAmount, uint256 seed) public {
        _activateBoundedMultiplier(seed);

        uint256 roundTrip = token.fromUIAmount(token.toUIAmount(rawAmount));
        require(roundTrip <= rawAmount);
    }

    function testFuzz_ConversionsAreMonotonic(
        uint128 rawA,
        uint128 rawB,
        uint128 uiA,
        uint128 uiB,
        uint256 seed
    ) public {
        _activateBoundedMultiplier(seed);

        uint256 lowerRaw = rawA < rawB ? rawA : rawB;
        uint256 upperRaw = rawA < rawB ? rawB : rawA;
        uint256 lowerUI = uiA < uiB ? uiA : uiB;
        uint256 upperUI = uiA < uiB ? uiB : uiA;

        require(token.toUIAmount(lowerRaw) <= token.toUIAmount(upperRaw));
        require(token.fromUIAmount(lowerUI) <= token.fromUIAmount(upperUI));
    }

    function testFuzz_ToUIFloorAdditivity(uint128 rawA, uint128 rawB, uint256 seed) public {
        _activateBoundedMultiplier(seed);

        uint256 separate = token.toUIAmount(rawA) + token.toUIAmount(rawB);
        uint256 combined = token.toUIAmount(uint256(rawA) + uint256(rawB));

        require(separate <= combined);
        require(combined <= separate + 1);
    }

    function testFuzz_UIViewsDelegateToConversion(uint128 mintedAmount, uint256 seed) public {
        _activateBoundedMultiplier(seed);

        vm.prank(ISSUER);
        require(token.mint(mintedAmount));

        require(token.balanceOfUI(ISSUER) == token.toUIAmount(token.balanceOf(ISSUER)));
        require(token.totalSupplyUI() == token.toUIAmount(token.totalSupply()));
    }

    function testFuzz_MultiplierSchedulingAndActivationPreserveRawAccounting(
        uint128 mintedAmount,
        uint256 seed
    ) public {
        vm.prank(ISSUER);
        require(token.mint(mintedAmount));

        uint256 balanceBefore = token.balanceOf(ISSUER);
        uint256 supplyBefore = token.totalSupply();
        uint256 multiplier = _boundedMultiplier(seed);
        uint256 effectiveAtTimestamp = block.timestamp + 1;

        vm.prank(ISSUER);
        token.setUIMultiplier(multiplier, effectiveAtTimestamp);

        require(token.balanceOf(ISSUER) == balanceBefore);
        require(token.totalSupply() == supplyBefore);

        vm.warp(effectiveAtTimestamp);

        require(token.uiMultiplier() == multiplier);
        require(token.balanceOf(ISSUER) == balanceBefore);
        require(token.totalSupply() == supplyBefore);
    }

    function test_ZeroConversionsAreZero() public view {
        require(token.toUIAmount(0) == 0);
        require(token.fromUIAmount(0) == 0);
    }

    function _activateBoundedMultiplier(uint256 seed) private returns (uint256 multiplier) {
        multiplier = _boundedMultiplier(seed);
        uint256 effectiveAtTimestamp = block.timestamp + 1;

        vm.prank(ISSUER);
        token.setUIMultiplier(multiplier, effectiveAtTimestamp);
        vm.warp(effectiveAtTimestamp);

        require(token.uiMultiplier() == multiplier);
    }

    function _boundedMultiplier(uint256 seed) private pure returns (uint256) {
        return MIN_MULTIPLIER + (seed % (MAX_MULTIPLIER - MIN_MULTIPLIER + 1));
    }

    function _selector(bytes memory returnData) private pure returns (bytes4 selector) {
        if (returnData.length < 4) return bytes4(0);
        assembly {
            selector := mload(add(returnData, 0x20))
        }
    }
}
