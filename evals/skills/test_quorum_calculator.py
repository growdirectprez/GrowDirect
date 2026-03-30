"""Quorum Calculator eval suite — 85% binary/regex + 15% LLM-as-judge.

Source material:
  - WPBCA Bylaws §5.9 (secret ballot — no quorum required)
  - WPBCA Bylaws §6.6.1.a (assessment quorum — 1/2 of members)
  - WPBCA Bylaws §6.6.1.b (director removal quorum — 1/3 of members)
  - WPBCA Bylaws §6.6.1.c (general quorum — 1/3 of members)
  - WPBCA Bylaws §8.9 (director election — secret ballot, no quorum)
  - WPBCA Bylaws §8.13 (tie-breaking — coin flip)
  - WPBCA Bylaws §8.20 (director removal — 1/3 quorum, majority vote)
  - WPBCA Bylaws §9.13 (board meeting quorum — majority of board)
  - WPBCA Bylaws §13.2 (special assessment — 1/2 quorum, majority vote)
  - WPBCA Bylaws §18.1 (bylaw amendment — secret ballot, no quorum)
  - AB 2460 (2024) — reconvened election quorum reduced to 20%
  - AB 2159 (2024) — electronic voting excludes special assessments
  - AB 502 (2022) — election by acclamation for uncontested seats
  - wpbca-bylaws-config.json — authoritative governance rules

Eval target: 90%+ pass rate.
  ~85% binary/regex checks (thresholds, math, citations)
  ~15% LLM-as-judge (compliance reasoning — tested separately)
"""

import importlib.util
import json
import math
import os
import sys

import pytest

COVE_ROOT = os.path.join(os.path.expanduser("~/GrowDirect"), "Cove")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

CONFIG_PATH = os.path.join(
    COVE_ROOT, "cove", "governance", "wpbca-bylaws-config.json"
)


@pytest.fixture
def bylaws_config():
    """Load the authoritative bylaws config."""
    with open(CONFIG_PATH) as f:
        return json.load(f)


@pytest.fixture
def total_lots(bylaws_config):
    """Total lots in WPBCA."""
    return bylaws_config["total_lots"]


@pytest.fixture
def quorum_calculator():
    """Import QuorumCalculator directly — bypasses cove/__init__.py (Flask)."""
    spec = importlib.util.spec_from_file_location(
        "quorum",
        os.path.join(COVE_ROOT, "cove", "governance", "quorum.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QuorumCalculator


# ---------------------------------------------------------------------------
# 1. Config integrity — verify bylaws config has all required fields
#    Source: wpbca-bylaws-config.json
# ---------------------------------------------------------------------------

class TestConfigIntegrity:
    """Bylaws config must have all required quorum data."""

    def test_total_lots_is_81(self, bylaws_config):
        """WPBCA has exactly 81 lots.

        Source: Bylaws — Tract 14649, 81 lots
        """
        assert bylaws_config["total_lots"] == 81

    def test_all_seven_proposal_types_exist(self, bylaws_config):
        """Config declares all 7 proposal types.

        Source: wpbca-bylaws-config.json
        """
        expected = {
            "resolution", "bylaw_amendment", "ccr_amendment",
            "election", "operating_rule", "special_assessment",
            "director_removal",
        }
        assert set(bylaws_config["proposal_types"].keys()) == expected

    def test_all_quorum_contexts_exist(self, bylaws_config):
        """Config declares all 5 quorum contexts.

        Source: wpbca-bylaws-config.json § quorum_rules
        """
        expected = {"general", "assessment", "secret_ballot", "reconvened", "board"}
        assert set(bylaws_config["quorum_rules"].keys()) == expected

    def test_proposal_types_have_required_fields(self, bylaws_config):
        """Each proposal type has threshold, quorum, and ballot fields."""
        required_fields = {
            "threshold", "quorum_required", "requires_secret_ballot",
            "notice_period_days",
        }
        for ptype, config in bylaws_config["proposal_types"].items():
            for field in required_fields:
                assert field in config, f"{ptype} missing field: {field}"


# ---------------------------------------------------------------------------
# 2. Quorum threshold accuracy — exact values from bylaws
#    Source: Bylaws §5.9, §6.6.1.a-c, §9.13, AB 2460
# ---------------------------------------------------------------------------

class TestQuorumThresholds:
    """Quorum thresholds must match bylaws exactly."""

    def test_general_quorum_is_one_third(self, bylaws_config):
        """General business quorum is 1/3 of members.

        Source: Bylaws §6.6.1.c — "the quorum shall be one third of the Members"
        """
        threshold = bylaws_config["quorum_rules"]["general"]["threshold"]
        assert abs(threshold - 1/3) < 0.01

    def test_assessment_quorum_is_one_half(self, bylaws_config):
        """Assessment vote quorum is 1/2 of members.

        Source: Bylaws §6.6.1.a — "the quorum requirement... shall be a majority of the Members"
        """
        threshold = bylaws_config["quorum_rules"]["assessment"]["threshold"]
        assert threshold == 0.50

    def test_secret_ballot_quorum_is_zero(self, bylaws_config):
        """Secret ballot votes require NO quorum.

        Source: Bylaws §5.9 — "A quorum is not required for votes with respect
        to which use of written secret ballot procedures... are mandatory"
        """
        threshold = bylaws_config["quorum_rules"]["secret_ballot"]["threshold"]
        assert threshold == 0.0

    def test_reconvened_quorum_is_twenty_percent(self, bylaws_config):
        """Reconvened election quorum is 20%.

        Source: AB 2460 (2024) — "Reconvened election quorum reduced to 20%"
        """
        threshold = bylaws_config["quorum_rules"]["reconvened"]["threshold"]
        assert threshold == 0.20

    def test_board_quorum_is_majority(self, bylaws_config):
        """Board meeting quorum is majority of board.

        Source: Bylaws §9.13 — "a majority of the number of directors
        authorized... shall constitute a quorum"
        """
        threshold = bylaws_config["quorum_rules"]["board"]["threshold"]
        assert threshold == 0.50


# ---------------------------------------------------------------------------
# 3. Quorum number calculation — math checks for 81 lots
#    Source: Bylaws + wpbca-bylaws-config.json total_lots = 81
# ---------------------------------------------------------------------------

class TestQuorumNumbers:
    """Quorum calculator produces correct member counts for 81 lots."""

    def test_general_quorum_count(self, quorum_calculator):
        """1/3 of 81 = 27 members needed.

        Source: §6.6.1.c, ceil(81 * 1/3) = 27
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("resolution")
        assert result.quorum_needed == 27

    def test_assessment_quorum_count(self, quorum_calculator):
        """1/2 of 81 = 41 members needed.

        Source: §6.6.1.a, ceil(81 * 0.5) = 41
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("special_assessment")
        assert result.quorum_needed == 41

    def test_election_quorum_count(self, quorum_calculator):
        """Elections (secret ballot) require 0 quorum.

        Source: §5.9 — no quorum for secret ballot
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election")
        assert result.quorum_needed == 0

    def test_bylaw_amendment_quorum_count(self, quorum_calculator):
        """Bylaw amendments (secret ballot) require 0 quorum.

        Source: §5.9 + §18.1
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("bylaw_amendment")
        assert result.quorum_needed == 0

    def test_ccr_amendment_quorum_count(self, quorum_calculator):
        """CC&R amendments (secret ballot) require 0 quorum.

        Source: §5.9 + §4270-4275
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("ccr_amendment")
        assert result.quorum_needed == 0

    def test_director_removal_quorum_count(self, quorum_calculator):
        """Director removal quorum is 1/3 = 27 members.

        Source: §6.6.1.b — "one third of the members"
        Note: §8.20 says it requires secret ballot, but §6.6.1.b
        explicitly sets 1/3 quorum for removal. The config uses
        quorum_required=0.33 for director_removal.
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("director_removal")
        assert result.quorum_needed == 27

    def test_reconvened_quorum_count(self, quorum_calculator):
        """Reconvened election quorum is 20% = 17 members.

        Source: AB 2460, ceil(81 * 0.20) = 17
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election", reconvened=True)
        assert result.quorum_needed == 17

    def test_board_quorum_count(self, quorum_calculator):
        """Board meeting quorum is majority of 5 = 3 directors.

        Source: §9.13, ceil(5 * 0.5) = 3
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate_board_quorum()
        assert result.quorum_needed == 3


# ---------------------------------------------------------------------------
# 4. Vote threshold accuracy — approval thresholds per type
#    Source: Bylaws §5.14, §13.2, §18.1, §4270-4275
# ---------------------------------------------------------------------------

class TestVoteThresholds:
    """Approval thresholds must match bylaws."""

    def test_resolution_threshold_is_majority(self, quorum_calculator):
        """Resolutions need majority (50%) of quorum.

        Source: §5.14 — "the affirmative vote of the majority of the
        voting power represented at the meeting"
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("resolution")
        assert result.approval_threshold == 0.50

    def test_ccr_amendment_threshold_is_supermajority(self, quorum_calculator):
        """CC&R amendments need 67% supermajority.

        Source: §4270-4275 — 2/3 supermajority
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("ccr_amendment")
        assert abs(result.approval_threshold - 0.67) < 0.01

    def test_election_threshold_is_plurality(self, quorum_calculator):
        """Elections use plurality (highest vote count wins).

        Source: §5.14 — "the candidates receiving the highest number
        of votes... shall be elected"
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election")
        assert result.approval_threshold == 0.0  # plurality = no threshold

    def test_special_assessment_threshold_is_majority(self, quorum_calculator):
        """Special assessment needs majority of quorum.

        Source: §13.2 — "approved by a majority of a quorum voting"
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("special_assessment")
        assert result.approval_threshold == 0.50


# ---------------------------------------------------------------------------
# 5. Secret ballot flag accuracy
#    Source: Bylaws §5.9
# ---------------------------------------------------------------------------

class TestSecretBallotFlags:
    """Secret ballot requirement must match bylaws §5.9."""

    @pytest.mark.parametrize("proposal_type,expected", [
        ("resolution", False),
        ("bylaw_amendment", True),
        ("ccr_amendment", True),
        ("election", True),
        ("operating_rule", False),
        ("special_assessment", True),
        ("director_removal", True),
    ])
    def test_secret_ballot_flag(self, quorum_calculator, proposal_type, expected):
        """Source: §5.9 — elections, amendments, assessments, removal require secret ballot."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate(proposal_type)
        assert result.requires_secret_ballot == expected


# ---------------------------------------------------------------------------
# 6. Electronic voting eligibility (AB 2159)
#    Source: AB 2159 (2024) — excludes special assessments
# ---------------------------------------------------------------------------

class TestElectronicVoting:
    """Electronic voting rules per AB 2159."""

    def test_special_assessment_not_electronic(self, quorum_calculator):
        """Special assessments cannot use electronic ballots.

        Source: AB 2159 — "excludes special assessments from electronic voting"
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("special_assessment")
        assert result.electronic_eligible is False

    def test_election_is_electronic_eligible(self, quorum_calculator):
        """Elections can use electronic ballots.

        Source: AB 2159 — electronic secret ballot voting
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election")
        assert result.electronic_eligible is True

    def test_operating_rule_not_electronic(self, quorum_calculator):
        """Operating rules are board-only, not electronic ballot.

        Source: wpbca-bylaws-config.json — operating_rule.electronic_eligible = false
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("operating_rule")
        assert result.electronic_eligible is False


# ---------------------------------------------------------------------------
# 7. Notice period accuracy
#    Source: Bylaws §6.4.2, §8.10, §8.20.1
# ---------------------------------------------------------------------------

class TestNoticePeriods:
    """Notice periods must match bylaws."""

    @pytest.mark.parametrize("proposal_type,expected_days", [
        ("resolution", 4),               # §9.1 — board meeting notice
        ("bylaw_amendment", 28),          # §18.1 — 28-day notice
        ("ccr_amendment", 28),            # §4270 — 28-day notice
        ("election", 28),                 # §8.10 — 30-day ballot delivery
        ("operating_rule", 28),           # §4340 — 28-day notice
        ("special_assessment", 28),       # §13.2 — 28-day notice
        ("director_removal", 35),         # §8.20.1(b) — 35-day notice
    ])
    def test_notice_period(self, quorum_calculator, proposal_type, expected_days):
        """Notice periods from bylaws config."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate(proposal_type)
        assert result.notice_period_days == expected_days


# ---------------------------------------------------------------------------
# 8. Bylaw citation accuracy
#    Source: exact section numbers from bylaws
# ---------------------------------------------------------------------------

class TestBylawCitations:
    """Quorum results must cite correct bylaw sections."""

    def test_general_cites_section_6_6_1_c(self, quorum_calculator):
        """General quorum citation references §6.6."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("resolution")
        assert "6.6" in result.quorum_citation

    def test_assessment_cites_section_6_6_1_a(self, quorum_calculator):
        """Assessment quorum cites §6.6.1.a."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("special_assessment")
        assert "13.2" in result.bylaw_section or "6.6" in result.bylaw_section

    def test_secret_ballot_cites_section_5_9(self, quorum_calculator):
        """Secret ballot quorum cites §5.9."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election")
        assert "5.9" in result.quorum_citation or "8.9" in result.bylaw_section

    def test_reconvened_cites_ab_2460(self, quorum_calculator):
        """Reconvened quorum cites AB 2460."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election", reconvened=True)
        assert "2460" in result.quorum_citation


# ---------------------------------------------------------------------------
# 9. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Boundary conditions and special cases."""

    def test_unknown_proposal_type_raises(self, quorum_calculator):
        """Unknown proposal type raises ValueError."""
        calc = quorum_calculator(total_lots=81)
        with pytest.raises(ValueError, match="Unknown proposal type"):
            calc.calculate("nonexistent_type")

    def test_zero_lots_returns_zero_quorum(self, quorum_calculator):
        """Edge case: 0 lots = 0 quorum needed."""
        calc = quorum_calculator(total_lots=0)
        result = calc.calculate("resolution")
        assert result.quorum_needed == 0

    def test_single_lot_general_quorum(self, quorum_calculator):
        """Edge case: 1 lot, ceil(1 * 0.33) = 1."""
        calc = quorum_calculator(total_lots=1)
        result = calc.calculate("resolution")
        assert result.quorum_needed == 1

    def test_quorum_met_check_true(self, quorum_calculator):
        """Quorum met check returns True when enough members present."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("resolution", members_present=30)
        assert result.quorum_met is True  # 30 >= 27

    def test_quorum_met_check_false(self, quorum_calculator):
        """Quorum met check returns False when not enough members."""
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("resolution", members_present=20)
        assert result.quorum_met is False  # 20 < 27

    def test_quorum_always_met_for_secret_ballot(self, quorum_calculator):
        """Secret ballot quorum is always met (0 required).

        Source: §5.9
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("election", members_present=0)
        assert result.quorum_met is True

    def test_approval_votes_needed_for_assessment(self, quorum_calculator):
        """With 50 members present at assessment vote, need 26 yes votes.

        Source: §13.2 — majority of quorum voting
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.calculate("special_assessment", members_present=50)
        assert result.votes_needed_to_pass == 26  # ceil(50 * 0.5)


# ---------------------------------------------------------------------------
# 10. Acclamation (AB 502)
# ---------------------------------------------------------------------------

class TestAcclamation:
    """AB 502 — election by acclamation for uncontested seats."""

    def test_uncontested_election_by_acclamation(self, quorum_calculator):
        """When candidates <= seats, election decided without ballot.

        Source: AB 502 (2022)
        """
        calc = quorum_calculator(total_lots=81)
        result = calc.check_acclamation(candidates=3, seats=5)
        assert result.acclamation is True

    def test_contested_election_requires_ballot(self, quorum_calculator):
        """When candidates > seats, normal ballot required."""
        calc = quorum_calculator(total_lots=81)
        result = calc.check_acclamation(candidates=7, seats=5)
        assert result.acclamation is False
