// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EvidenceRegistry {

    struct EvidenceRecord {
        address submittedBy;
        uint256 timestamp;
        bool exists;
    }

    mapping(bytes32 => EvidenceRecord) private evidenceRecords;

    event EvidenceRegistered(
        bytes32 indexed evidenceHash,
        address indexed submittedBy,
        uint256 timestamp
    );

    function registerEvidence(bytes32 evidenceHash) external {

        require(
            !evidenceRecords[evidenceHash].exists,
            "Evidence already registered"
        );

        evidenceRecords[evidenceHash] = EvidenceRecord({
            submittedBy: msg.sender,
            timestamp: block.timestamp,
            exists: true
        });

        emit EvidenceRegistered(
            evidenceHash,
            msg.sender,
            block.timestamp
        );
    }

    function verifyEvidence(
        bytes32 evidenceHash
    )
        external
        view
        returns (
            bool exists,
            address submittedBy,
            uint256 timestamp
        )
    {
        EvidenceRecord memory record =
            evidenceRecords[evidenceHash];

        return (
            record.exists,
            record.submittedBy,
            record.timestamp
        );
    }
}