// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ICompliance} from "src/scaledUIToken/compliance/ICompliance.sol";
import {IPauseManager} from "src/scaledUIToken/pauseManager/IPauseManager.sol";

/// Deterministic policy contracts used only to make the verification
/// environment explicit. They are not production implementations.
contract AlwaysUnpausedPauseManager is IPauseManager {
    function isTokenPaused(address) external pure returns (bool) {
        return false;
    }
}

contract AlwaysPausedPauseManager is IPauseManager {
    function isTokenPaused(address) external pure returns (bool) {
        return true;
    }
}

contract AlwaysCompliantCompliance is ICompliance {
    function checkIsCompliant(address, address) external pure {}
}

contract RejectAllCompliance is ICompliance {
    function checkIsCompliant(address, address) external pure {
        revert("not compliant");
    }
}
