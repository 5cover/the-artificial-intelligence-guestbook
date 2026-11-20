from datetime import UTC, datetime, timedelta

import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Account, MagicLink
from moderation.models import ModerationRecord
from testimonies.models import ConsentRecord, Revision, Testimony

NOW = datetime(2027, 3, 14, 9, 30, tzinfo=UTC)
PUBLIC_ID = "7q4km2xd"


def make_account(email="someone@example.org"):
    return Account.objects.create(email=email, created_at=NOW)


def make_revision(testimony, **overrides):
    values = {"sequence": 1, "submitted_at": NOW}
    values.update(overrides)
    return Revision.objects.create(testimony=testimony, **values)


def assert_violates(constraint, create):
    with pytest.raises(IntegrityError) as error, transaction.atomic():
        create()
    assert constraint in str(error.value)


def submitted(**overrides):
    values = {
        "state": "submitted",
        "received_at": NOW,
        "language": "en",
        "edition_period": 2027,
    }
    values.update(overrides)
    return values


@pytest.mark.django_db
def test_a_valid_draft_and_a_submitted_testimony_are_accepted():
    Testimony.objects.create()
    Testimony.objects.create(**submitted())


@pytest.mark.django_db
def test_one_testimony_per_account():
    account = make_account()
    Testimony.objects.create(account=account)
    with pytest.raises(IntegrityError), transaction.atomic():
        Testimony.objects.create(account=account)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("constraint", "values"),
    [
        ("testimony_public_id_pattern", {"public_id": "7Q4KM2XD", "published_at": NOW}),
        ("testimony_language_is_bcp47", {"language": "not a tag!"}),
        ("testimony_edition_period_from_2026", {"edition_period": 2025}),
        ("testimony_state_enum", submitted(state="bogus")),
        ("testimony_public_id_iff_published", {"public_id": PUBLIC_ID}),
        ("testimony_withdrawn_iff_withdrawn_at", {"withdrawn_at": NOW}),
        ("testimony_submitted_has_receipt_language_and_period", {"state": "submitted"}),
        (
            "testimony_period_is_utc_year_of_receipt",
            {
                "received_at": NOW,
                "edition_period": 2026,
                "state": "submitted",
                "language": "en",
            },
        ),
        ("testimony_quarantine_iff_reason", submitted(state="quarantined")),
        (
            "testimony_published_has_revisions",
            submitted(state="published", public_id=PUBLIC_ID, published_at=NOW),
        ),
    ],
)
def test_testimony_rejects_invalid_states(constraint, values):
    assert_violates(constraint, lambda: Testimony.objects.create(**values))


@pytest.mark.django_db
def test_published_or_withdrawn_testimonies_need_a_public_id():
    assert_violates(
        "testimony_published_states_have_public_id",
        lambda: Testimony.objects.create(
            **submitted(state="withdrawn", withdrawn_at=NOW)
        ),
    )


@pytest.mark.django_db
def test_withdrawn_testimonies_have_no_account():
    account = make_account()
    assert_violates(
        "testimony_withdrawn_has_no_account",
        lambda: Testimony.objects.create(
            account=account,
            **submitted(
                state="withdrawn",
                withdrawn_at=NOW,
                public_id=PUBLIC_ID,
                published_at=NOW,
            ),
        ),
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field",
    ["state", "quarantine_reason", "language", "edition_period"],
)
def test_database_rejects_values_outside_each_enumeration(field):
    testimony = Testimony.objects.create()
    value = {
        "state": "bogus",
        "quarantine_reason": "bogus",
        "language": "bad tag!",
        "edition_period": 1999,
    }[field]
    with pytest.raises(IntegrityError), transaction.atomic():
        Testimony.objects.filter(pk=testimony.pk).update(**{field: value})


@pytest.mark.django_db
def test_revision_sequence_and_number_are_unique_per_testimony():
    testimony = Testimony.objects.create()
    make_revision(testimony, sequence=1)
    with pytest.raises(IntegrityError), transaction.atomic():
        make_revision(testimony, sequence=1)


@pytest.mark.django_db
def test_revision_numbers_are_unique_per_testimony():
    testimony = Testimony.objects.create()
    make_revision(testimony, sequence=1, revision_number=1, live_at=NOW)
    with pytest.raises(IntegrityError), transaction.atomic():
        make_revision(testimony, sequence=2, revision_number=1, live_at=NOW)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("constraint", "overrides"),
    [
        ("revision_number_iff_live", {"revision_number": 1}),
        ("revision_reviewed_iff_not_pending", {"review_state": "approved"}),
        ("revision_body_length", {"body": ""}),
        ("revision_body_length", {"body": "x" * 50001}),
        (
            "revision_identity_mode_enum",
            {"identity_mode": "bogus", "display_name": "X"},
        ),
        (
            "revision_anonymous_iff_no_display_name",
            {"identity_mode": "anonymous", "display_name": "X"},
        ),
        ("revision_age_range_enum", {"age_range": "bogus"}),
        ("revision_organization_type_enum", {"organization_type": "bogus"}),
        ("revision_field_enum", {"field": "bogus"}),
        ("revision_ai_use_frequency_enum", {"ai_use_frequency": "bogus"}),
        ("revision_attitude_enum", {"attitude": "bogus"}),
        ("revision_authorship_category_enum", {"authorship_category": "bogus"}),
        ("revision_country_is_iso_alpha2", {"country": "fr"}),
        ("revision_relationship_to_ai_codes", {"relationship_to_ai": ["bogus"]}),
        (
            "revision_relationship_to_ai_is_a_set",
            {"relationship_to_ai": ["user", "user"]},
        ),
        (
            "revision_no_authorship_details_without_ai",
            {"authorship_category": "none", "provider": "X"},
        ),
        ("revision_horizon_needs_prediction", {"prediction_horizon": 2030}),
    ],
)
def test_revision_rejects_invalid_content(constraint, overrides):
    testimony = Testimony.objects.create()
    if "identity_mode" in overrides and overrides["identity_mode"] == "anonymous":
        overrides = {**overrides, "display_name": "Named"}
    assert_violates(
        constraint,
        lambda: make_revision(testimony, **overrides),
    )


@pytest.mark.django_db
def test_returned_revisions_cite_a_moderation_record():
    testimony = Testimony.objects.create()
    assert_violates(
        "revision_returned_has_record",
        lambda: make_revision(testimony, review_state="returned", reviewed_at=NOW),
    )


@pytest.mark.django_db
def test_set_and_enumeration_checks_accept_valid_values():
    testimony = Testimony.objects.create()
    make_revision(
        testimony,
        identity_mode="named",
        display_name="Ada",
        relationship_to_ai=["user", "researcher"],
        country="FR",
        prediction="In five years.",
        prediction_horizon=2032,
    )


@pytest.mark.django_db
def test_consent_parental_path_matches_the_declared_age_band():
    testimony = Testimony.objects.create()
    revision = make_revision(testimony)
    assert_violates(
        "consent_parental_path_iff_under_16",
        lambda: ConsentRecord.objects.create(
            testimony=testimony,
            revision=revision,
            publication_consent_at=NOW,
            licence_grant_version="v",
            terms_version="v",
            privacy_notice_version="v",
            consent_locale="en",
            declared_age_band="16-or-over",
            consent_path="parental",
        ),
    )


@pytest.mark.django_db
def test_parental_consent_needs_the_parental_path():
    testimony = Testimony.objects.create()
    revision = make_revision(testimony)
    assert_violates(
        "consent_parental_consent_needs_parental_path",
        lambda: ConsentRecord.objects.create(
            testimony=testimony,
            revision=revision,
            publication_consent_at=NOW,
            licence_grant_version="v",
            terms_version="v",
            privacy_notice_version="v",
            consent_locale="en",
            declared_age_band="16-or-over",
            consent_path="self",
            parental_consent_at=NOW,
            parental_method="email-link",
        ),
    )


@pytest.mark.django_db
def test_parental_consent_time_and_method_go_together():
    testimony = Testimony.objects.create()
    revision = make_revision(testimony)
    assert_violates(
        "consent_parental_method_iff_consent",
        lambda: ConsentRecord.objects.create(
            testimony=testimony,
            revision=revision,
            publication_consent_at=NOW,
            licence_grant_version="v",
            terms_version="v",
            privacy_notice_version="v",
            consent_locale="en",
            declared_age_band="under-16",
            consent_path="parental",
            parental_method="email-link",
        ),
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("constraint", "values"),
    [
        (
            "moderation_returns_cite_a_rule",
            {"decision": "return", "guidance": "Change it."},
        ),
        (
            "moderation_returns_give_guidance",
            {"decision": "return", "rule": "third-party-privacy"},
        ),
    ],
)
def test_returns_need_a_rule_and_guidance(constraint, values):
    assert_violates(
        constraint,
        lambda: ModerationRecord.objects.create(
            decided_by="custodian", decided_at=NOW, **values
        ),
    )


@pytest.mark.django_db
def test_parental_links_belong_to_a_testimony():
    now = timezone.now()
    assert_violates(
        "magic_link_parental_has_testimony",
        lambda: MagicLink.objects.create(
            purpose="parental",
            token_hash=b"p" * 32,
            email="parent@example.org",
            created_at=now,
            expires_at=now + timedelta(minutes=15),
        ),
    )


@pytest.mark.django_db
def test_withdrawal_codes_exist_only_without_an_account():
    account = make_account("code@example.org")
    assert_violates(
        "testimony_codes_only_without_account",
        lambda: Testimony.objects.create(
            account=account, withdrawal_code_hash=b"c" * 32
        ),
    )
