from django.utils.translation import gettext_lazy as _

from testimonies.vocabularies import (
    AgeRange,
    AIUseFrequency,
    Attitude,
    AuthorshipCategory,
    Field,
    OrganizationType,
    RelationshipToAI,
)

# Display labels for the codes of a public record. Codes stay stable; labels
# are what readers see.
ENUMERATIONS = {
    "age_range": AgeRange,
    "organization_type": OrganizationType,
    "relationship_to_ai": RelationshipToAI,
    "field": Field,
    "category": AuthorshipCategory,
    "ai_use_frequency": AIUseFrequency,
    "attitude": Attitude,
}

IDENTITY_ROWS = (
    ("display_name", _("Display name, given by the contributor")),
    ("age_range", _("Age range")),
    ("country", _("Country")),
    ("region", _("Region")),
    ("languages", _("Languages lived in")),
    ("profession", _("Profession")),
    ("field", _("Field")),
    ("field_note", _("Field, in the contributor's words")),
    ("organization", _("Organization")),
    ("organization_type", _("Type of organization")),
    ("organization_type_note", _("Type of organization, in the contributor's words")),
    ("relationship_to_ai", _("Relationship to AI")),
    ("relationship_to_ai_note", _("Relationship to AI, in the contributor's words")),
    ("link", _("Link")),
)

AUTHORSHIP_ROWS = (
    ("category", _("AI involvement")),
    ("provider", _("AI provider")),
    ("product", _("AI product")),
    ("model", _("Model")),
    ("model_version", _("Model version")),
    ("mode_or_setting", _("Mode or setting")),
    ("inputs", _("Information the AI system received")),
    ("workflow", _("Prompts or workflow")),
    ("changes_after", _("Changes made afterwards")),
    ("comment", _("Comment")),
)

STRUCTURED_ROWS = (
    ("ai_use_frequency", _("How often AI is used")),
    ("tools_used", _("Tools used")),
    ("attitude", _("Attitude towards AI")),
    ("attitude_note", _("Attitude, in the contributor's words")),
    ("prediction", _("Prediction left on record")),
    ("prediction_horizon", _("Year the prediction is for")),
)


def display_value(name, value):
    enumeration = ENUMERATIONS.get(name)
    if isinstance(value, list):
        if enumeration is not None:
            return ", ".join(str(enumeration(item).label) for item in value)
        return ", ".join(str(item) for item in value)
    if enumeration is not None:
        return str(enumeration(value).label)
    return str(value)


def rows(section, labels):
    return [
        (label, display_value(name, section[name]))
        for name, label in labels
        if name in section
    ]
