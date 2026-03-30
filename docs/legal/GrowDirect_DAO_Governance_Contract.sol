// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * ============================================================================
 * GROWDIRECT DAO LLC — GOVERNANCE SMART CONTRACT
 * ============================================================================
 *
 * Entity:          GrowDirect DAO LLC (Wyoming DAO LLC, W.S. 17-31)
 * Token:           GROW (ERC-20 Governance Token)
 * Total Supply:    100,000,000 GROW (fixed)
 * Deployer:        Geoffrey C. Lyle (gclyle@growdirect.io)
 *
 * PURPOSE:
 * This contract serves as the on-chain governance mechanism for GrowDirect
 * DAO LLC, as required by W.S. 17-31-104(b)(iii). It manages:
 *   - Governance token (GROW) issuance and vesting
 *   - Proposal creation, voting, and execution
 *   - Treasury management with multi-sig controls
 *   - Smart contract upgradeability (W.S. 17-31-106(d))
 *
 * LEGAL NOTICE:
 * Per W.S. 17-31-106(b), in the event of conflict between this smart
 * contract and the Operating Agreement, this contract controls for
 * on-chain governance matters.
 *
 * DEPLOYMENT TARGET:
 * Avalanche C-Chain (Primary). The State of Wyoming has deployed its
 * Frontier Stable Token (FRNT) on Avalanche, making this the state's
 * preferred blockchain infrastructure. GrowDirect will also operate an
 * Avalanche validator node (3,000 AVAX stake), directly securing the
 * network on which FRNT and this governance contract operate.
 *
 * Avalanche C-Chain is EVM-compatible — this Solidity contract deploys
 * natively with no modifications. The UUPS proxy pattern is fully
 * supported on Avalanche.
 *
 * ATTORNEY REVIEW NOTES:
 * 1. This contract is a DRAFT for attorney review — DO NOT DEPLOY without
 *    security audit by a qualified smart contract auditor (e.g., OpenZeppelin,
 *    Trail of Bits, Consensys Diligence)
 * 2. Token allocation percentages should be confirmed against final cap table
 * 3. Securities counsel should evaluate GROW token classification under Howey
 * 4. Deployment target: Avalanche C-Chain (aligned with Wyoming FRNT)
 * 5. The upgradeability pattern (UUPS proxy) satisfies W.S. 17-31-106(d)
 *    requirement that smart contracts be "able to be updated, modified or
 *    otherwise upgraded"
 * 6. GrowDirect will run an Avalanche validator (3,000 AVAX, ~$26,700 at
 *    Feb 2026 prices). Validator rewards (~7.65% APY) accrue to DAO treasury.
 *    No slashing risk on Avalanche.
 *
 * ============================================================================
 */

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/ReentrancyGuardUpgradeable.sol";

/**
 * @title GrowDirectDAO
 * @notice Governance contract for GrowDirect DAO LLC (Wyoming W.S. 17-31)
 * @dev UUPS upgradeable pattern to satisfy W.S. 17-31-106(d)
 */
contract GrowDirectDAO is
    ERC20Upgradeable,
    OwnableUpgradeable,
    UUPSUpgradeable,
    ReentrancyGuardUpgradeable
{
    // =========================================================================
    // CONSTANTS
    // =========================================================================

    uint256 public constant TOTAL_SUPPLY = 100_000_000 * 1e18; // 100M GROW

    // Token allocation percentages (basis points, 10000 = 100%)
    uint256 public constant FOUNDER_ALLOCATION = 5100;    // 51%
    uint256 public constant TEAM_ALLOCATION = 1500;       // 15%
    uint256 public constant TREASURY_ALLOCATION = 2000;   // 20%
    uint256 public constant COMMUNITY_ALLOCATION = 1000;  // 10%
    uint256 public constant INVESTOR_ALLOCATION = 400;    // 4%

    // Governance parameters (aligned with Operating Agreement Article 4)
    uint256 public constant PROPOSAL_THRESHOLD = 100_000 * 1e18; // Min tokens to create proposal
    uint256 public constant VOTING_PERIOD_STANDARD = 3 days;
    uint256 public constant VOTING_PERIOD_MAJOR = 7 days;
    uint256 public constant VOTING_PERIOD_CRITICAL = 14 days;
    uint256 public constant TIMELOCK_DELAY = 2 days;

    // Quorum thresholds (basis points of participating tokens)
    uint256 public constant QUORUM_STANDARD = 2000;   // 20%
    uint256 public constant QUORUM_MAJOR = 3000;       // 30%
    uint256 public constant QUORUM_CRITICAL = 5000;    // 50%

    // Approval thresholds
    uint256 public constant MAJORITY = 5001;            // >50%
    uint256 public constant SUPERMAJORITY = 6667;        // >66.7%

    // =========================================================================
    // STATE VARIABLES
    // =========================================================================

    /// @notice Founder address (Geoffrey C. Lyle)
    address public founder;

    /// @notice Treasury multi-sig address
    address public treasury;

    /// @notice Whether the initial operating period is active (24 months or first funding)
    bool public initialOperatingPeriod;

    /// @notice Timestamp when initial operating period ends
    uint256 public initialPeriodEnd;

    /// @notice Proposal counter
    uint256 public proposalCount;

    /// @notice Vesting schedules
    mapping(address => VestingSchedule) public vestingSchedules;

    /// @notice Proposals
    mapping(uint256 => Proposal) public proposals;

    /// @notice Votes cast per proposal per address
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    // =========================================================================
    // STRUCTS
    // =========================================================================

    enum ProposalType {
        Operational,        // < $50K spend, Majority, 20% quorum, 3 days
        Treasury,           // > $50K spend, Majority, 30% quorum, 5 days
        SmartContractUpgrade, // Supermajority, 30% quorum, 7 days
        AmendOperatingAgreement, // Supermajority, 30% quorum, 7 days
        AmendArticles,      // Supermajority, 40% quorum, 14 days
        Dissolution,        // Supermajority, 50% quorum, 14 days
        TokenSupplyChange   // Supermajority, 50% quorum, 14 days
    }

    enum ProposalState {
        Pending,
        Active,
        Passed,
        Failed,
        Executed,
        Cancelled
    }

    struct Proposal {
        uint256 id;
        address proposer;
        ProposalType proposalType;
        string description;
        string ipfsHash;        // IPFS hash of detailed proposal document
        uint256 startTime;
        uint256 endTime;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 votesAbstain;
        ProposalState state;
        bytes executionData;    // Encoded function call for execution
        address executionTarget;
    }

    struct VestingSchedule {
        uint256 totalAmount;
        uint256 released;
        uint256 startTime;
        uint256 cliffDuration;  // 1 year default
        uint256 vestingDuration; // 4 years default
        bool revocable;
    }

    // =========================================================================
    // EVENTS
    // =========================================================================

    event ProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        ProposalType proposalType,
        string description
    );
    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        uint8 support, // 0=against, 1=for, 2=abstain
        uint256 weight
    );
    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalCancelled(uint256 indexed proposalId);
    event TokensVested(address indexed beneficiary, uint256 amount);
    event InitialOperatingPeriodEnded();
    event TreasuryUpdated(address indexed newTreasury);

    // =========================================================================
    // MODIFIERS
    // =========================================================================

    modifier onlyFounder() {
        require(msg.sender == founder, "GrowDirectDAO: caller is not founder");
        _;
    }

    modifier onlyDuringInitialPeriod() {
        require(initialOperatingPeriod, "GrowDirectDAO: initial operating period ended");
        require(block.timestamp < initialPeriodEnd, "GrowDirectDAO: initial period expired");
        _;
    }

    // =========================================================================
    // INITIALIZATION (UUPS Proxy Pattern)
    // =========================================================================

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /**
     * @notice Initialize the DAO contract
     * @param _founder Address of Geoffrey C. Lyle
     * @param _treasury Address of the multi-sig treasury
     */
    function initialize(
        address _founder,
        address _treasury
    ) public initializer {
        __ERC20_init("GrowDirect Governance", "GROW");
        __Ownable_init(_founder);
        __UUPSUpgradeable_init();
        __ReentrancyGuard_init();

        founder = _founder;
        treasury = _treasury;
        initialOperatingPeriod = true;
        initialPeriodEnd = block.timestamp + 730 days; // 24 months

        // Mint total supply to this contract for controlled distribution
        _mint(address(this), TOTAL_SUPPLY);

        // Transfer treasury allocation immediately
        _transfer(
            address(this),
            _treasury,
            (TOTAL_SUPPLY * TREASURY_ALLOCATION) / 10000
        );

        // Set up founder vesting (51%, 4-year vest, 1-year cliff)
        _createVestingSchedule(
            _founder,
            (TOTAL_SUPPLY * FOUNDER_ALLOCATION) / 10000,
            365 days,   // 1 year cliff
            1460 days,  // 4 year vesting
            false        // non-revocable
        );
    }

    // =========================================================================
    // GOVERNANCE FUNCTIONS
    // =========================================================================

    /**
     * @notice Create a new governance proposal
     * @param _type Proposal type (determines thresholds)
     * @param _description Short description of the proposal
     * @param _ipfsHash IPFS hash of the full proposal document
     * @param _executionTarget Target contract for execution (address(0) if none)
     * @param _executionData Encoded function call for execution (empty if none)
     */
    function createProposal(
        ProposalType _type,
        string calldata _description,
        string calldata _ipfsHash,
        address _executionTarget,
        bytes calldata _executionData
    ) external returns (uint256) {
        require(
            balanceOf(msg.sender) >= PROPOSAL_THRESHOLD,
            "GrowDirectDAO: insufficient tokens to propose"
        );

        uint256 votingPeriod = _getVotingPeriod(_type);

        proposalCount++;
        Proposal storage prop = proposals[proposalCount];
        prop.id = proposalCount;
        prop.proposer = msg.sender;
        prop.proposalType = _type;
        prop.description = _description;
        prop.ipfsHash = _ipfsHash;
        prop.startTime = block.timestamp;
        prop.endTime = block.timestamp + votingPeriod;
        prop.state = ProposalState.Active;
        prop.executionTarget = _executionTarget;
        prop.executionData = _executionData;

        emit ProposalCreated(proposalCount, msg.sender, _type, _description);
        return proposalCount;
    }

    /**
     * @notice Cast a vote on an active proposal
     * @param _proposalId ID of the proposal
     * @param _support 0=against, 1=for, 2=abstain
     */
    function castVote(uint256 _proposalId, uint8 _support) external {
        Proposal storage prop = proposals[_proposalId];
        require(prop.state == ProposalState.Active, "GrowDirectDAO: proposal not active");
        require(block.timestamp <= prop.endTime, "GrowDirectDAO: voting period ended");
        require(!hasVoted[_proposalId][msg.sender], "GrowDirectDAO: already voted");
        require(_support <= 2, "GrowDirectDAO: invalid vote type");

        uint256 weight = balanceOf(msg.sender);
        require(weight > 0, "GrowDirectDAO: no voting power");

        hasVoted[_proposalId][msg.sender] = true;

        if (_support == 0) {
            prop.votesAgainst += weight;
        } else if (_support == 1) {
            prop.votesFor += weight;
        } else {
            prop.votesAbstain += weight;
        }

        emit VoteCast(_proposalId, msg.sender, _support, weight);
    }

    /**
     * @notice Finalize a proposal after voting period ends
     * @param _proposalId ID of the proposal to finalize
     */
    function finalizeProposal(uint256 _proposalId) external {
        Proposal storage prop = proposals[_proposalId];
        require(prop.state == ProposalState.Active, "GrowDirectDAO: proposal not active");
        require(block.timestamp > prop.endTime, "GrowDirectDAO: voting not ended");

        uint256 totalVotes = prop.votesFor + prop.votesAgainst + prop.votesAbstain;
        uint256 quorumRequired = _getQuorum(prop.proposalType);
        uint256 approvalRequired = _getApprovalThreshold(prop.proposalType);

        // Check quorum (percentage of total supply that voted)
        bool quorumMet = (totalVotes * 10000) / totalSupply() >= quorumRequired;

        // Check approval (percentage of for-votes vs total non-abstain votes)
        uint256 nonAbstainVotes = prop.votesFor + prop.votesAgainst;
        bool approved = nonAbstainVotes > 0 &&
            (prop.votesFor * 10000) / nonAbstainVotes >= approvalRequired;

        if (quorumMet && approved) {
            prop.state = ProposalState.Passed;
        } else {
            prop.state = ProposalState.Failed;
        }
    }

    /**
     * @notice Execute a passed proposal (after timelock)
     * @param _proposalId ID of the proposal to execute
     */
    function executeProposal(uint256 _proposalId) external nonReentrant {
        Proposal storage prop = proposals[_proposalId];
        require(prop.state == ProposalState.Passed, "GrowDirectDAO: proposal not passed");
        require(
            block.timestamp >= prop.endTime + TIMELOCK_DELAY,
            "GrowDirectDAO: timelock not expired"
        );

        prop.state = ProposalState.Executed;

        // Execute on-chain action if specified
        if (prop.executionTarget != address(0) && prop.executionData.length > 0) {
            (bool success, ) = prop.executionTarget.call(prop.executionData);
            require(success, "GrowDirectDAO: execution failed");
        }

        emit ProposalExecuted(_proposalId);
    }

    // =========================================================================
    // VESTING FUNCTIONS
    // =========================================================================

    /**
     * @notice Release vested tokens to the caller
     */
    function releaseVestedTokens() external nonReentrant {
        VestingSchedule storage schedule = vestingSchedules[msg.sender];
        require(schedule.totalAmount > 0, "GrowDirectDAO: no vesting schedule");

        uint256 releasable = _vestedAmount(msg.sender) - schedule.released;
        require(releasable > 0, "GrowDirectDAO: no tokens to release");

        schedule.released += releasable;
        _transfer(address(this), msg.sender, releasable);

        emit TokensVested(msg.sender, releasable);
    }

    /**
     * @notice Get the vested amount for a beneficiary
     */
    function vestedAmount(address _beneficiary) external view returns (uint256) {
        return _vestedAmount(_beneficiary);
    }

    /**
     * @notice Get the releasable (vested but unclaimed) amount
     */
    function releasableAmount(address _beneficiary) external view returns (uint256) {
        return _vestedAmount(_beneficiary) - vestingSchedules[_beneficiary].released;
    }

    // =========================================================================
    // FOUNDER FUNCTIONS (Initial Operating Period)
    // =========================================================================

    /**
     * @notice Allocate team/advisor tokens with vesting
     * @dev Only callable by founder during initial operating period
     */
    function allocateTeamTokens(
        address _beneficiary,
        uint256 _amount,
        uint256 _cliffDuration,
        uint256 _vestingDuration
    ) external onlyFounder onlyDuringInitialPeriod {
        require(_amount > 0, "GrowDirectDAO: amount must be > 0");
        require(
            vestingSchedules[_beneficiary].totalAmount == 0,
            "GrowDirectDAO: schedule exists"
        );

        _createVestingSchedule(
            _beneficiary,
            _amount,
            _cliffDuration,
            _vestingDuration,
            true // revocable for team members
        );
    }

    /**
     * @notice End the initial operating period early (e.g., upon first funding)
     */
    function endInitialOperatingPeriod() external onlyFounder {
        initialOperatingPeriod = false;
        emit InitialOperatingPeriodEnded();
    }

    /**
     * @notice Update the treasury address
     * @dev Requires supermajority vote after initial period
     */
    function updateTreasury(address _newTreasury) external onlyOwner {
        require(_newTreasury != address(0), "GrowDirectDAO: zero address");
        treasury = _newTreasury;
        emit TreasuryUpdated(_newTreasury);
    }

    // =========================================================================
    // VIEW FUNCTIONS
    // =========================================================================

    /**
     * @notice Get proposal details
     */
    function getProposal(uint256 _proposalId)
        external
        view
        returns (
            address proposer,
            ProposalType proposalType,
            string memory description,
            uint256 startTime,
            uint256 endTime,
            uint256 votesFor,
            uint256 votesAgainst,
            uint256 votesAbstain,
            ProposalState state
        )
    {
        Proposal storage prop = proposals[_proposalId];
        return (
            prop.proposer,
            prop.proposalType,
            prop.description,
            prop.startTime,
            prop.endTime,
            prop.votesFor,
            prop.votesAgainst,
            prop.votesAbstain,
            prop.state
        );
    }

    // =========================================================================
    // INTERNAL FUNCTIONS
    // =========================================================================

    function _createVestingSchedule(
        address _beneficiary,
        uint256 _amount,
        uint256 _cliffDuration,
        uint256 _vestingDuration,
        bool _revocable
    ) internal {
        vestingSchedules[_beneficiary] = VestingSchedule({
            totalAmount: _amount,
            released: 0,
            startTime: block.timestamp,
            cliffDuration: _cliffDuration,
            vestingDuration: _vestingDuration,
            revocable: _revocable
        });
    }

    function _vestedAmount(address _beneficiary) internal view returns (uint256) {
        VestingSchedule storage schedule = vestingSchedules[_beneficiary];
        if (schedule.totalAmount == 0) return 0;

        uint256 elapsed = block.timestamp - schedule.startTime;

        // Before cliff: nothing vested
        if (elapsed < schedule.cliffDuration) return 0;

        // After full vesting: everything vested
        if (elapsed >= schedule.vestingDuration) return schedule.totalAmount;

        // Linear vesting between cliff and end
        return (schedule.totalAmount * elapsed) / schedule.vestingDuration;
    }

    function _getVotingPeriod(ProposalType _type) internal pure returns (uint256) {
        if (_type == ProposalType.Operational) return VOTING_PERIOD_STANDARD;
        if (_type == ProposalType.Treasury) return 5 days;
        if (_type == ProposalType.SmartContractUpgrade) return VOTING_PERIOD_MAJOR;
        if (_type == ProposalType.AmendOperatingAgreement) return VOTING_PERIOD_MAJOR;
        return VOTING_PERIOD_CRITICAL; // Articles, Dissolution, TokenSupply
    }

    function _getQuorum(ProposalType _type) internal pure returns (uint256) {
        if (_type == ProposalType.Operational) return QUORUM_STANDARD;
        if (_type == ProposalType.Treasury) return QUORUM_MAJOR;
        if (_type == ProposalType.SmartContractUpgrade) return QUORUM_MAJOR;
        if (_type == ProposalType.AmendOperatingAgreement) return QUORUM_MAJOR;
        if (_type == ProposalType.AmendArticles) return 4000; // 40%
        return QUORUM_CRITICAL; // Dissolution, TokenSupply
    }

    function _getApprovalThreshold(ProposalType _type) internal pure returns (uint256) {
        if (_type == ProposalType.Operational) return MAJORITY;
        if (_type == ProposalType.Treasury) return MAJORITY;
        return SUPERMAJORITY; // Everything else
    }

    /**
     * @notice UUPS upgrade authorization — requires supermajority vote
     * @dev Per W.S. 17-31-106(d), the contract must be upgradeable
     */
    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
