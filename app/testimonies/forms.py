import re
import unicodedata

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from testimonies import vocabularies as vocab
from testimonies.models import BODY_MAX_LENGTH, LANGUAGE_PATTERN

LANGUAGE_TAG = re.compile(LANGUAGE_PATTERN)
ALLOWED_LINK_SCHEMES = ("http://", "https://")


def canonical_language(tag):
    parts = tag.split("-")
    canonical = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 2 and part.isalpha():
            canonical.append(part.upper())
        elif len(part) == 4 and part.isalpha():
            canonical.append(part.title())
        else:
            canonical.append(part.lower())
    return "-".join(canonical)


class TextField(forms.CharField):
    """Text in NFC with line feeds only where allowed and no other control characters."""

    def __init__(self, *, multiline=False, **kwargs):
        self.multiline = multiline
        super().__init__(**kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        return unicodedata.normalize("NFC", value).strip()

    def validate(self, value):
        super().validate(value)
        if not self.multiline and "\n" in value:
            raise ValidationError(_("Use a single line for this field."))
        if any(unicodedata.category(char) == "Cc" and char != "\n" for char in value):
            raise ValidationError(_("Remove control characters, such as tabs."))


class LanguageField(TextField):
    def validate(self, value):
        super().validate(value)
        if value and not LANGUAGE_TAG.match(value):
            raise ValidationError(_("Use a language tag such as en or fr-FR."))


class ContributionForm(forms.Form):
    language = LanguageField(
        max_length=35,
        required=False,
        label=_("Language of your testimony"),
        help_text=_("A language tag such as en or fr. Required before you submit."),
    )
    body = TextField(
        multiline=True,
        max_length=BODY_MAX_LENGTH,
        required=False,
        widget=forms.Textarea,
        label=_("Your testimony"),
        help_text=_(
            "Plain text with CommonMark formatting. Raw HTML is shown as text, "
            "and images are shown as their description."
        ),
    )

    identity_mode = forms.ChoiceField(
        choices=vocab.IdentityMode.choices,
        widget=forms.RadioSelect,
        initial=vocab.IdentityMode.ANONYMOUS,
        label=_("How your testimony is attributed"),
    )
    display_name = TextField(
        max_length=100,
        required=False,
        label=_("Display name"),
        help_text=_("The name you choose. It is not verified."),
    )
    age_range = forms.ChoiceField(
        choices=[("", _("Not given")), *vocab.AgeRange.choices],
        required=False,
        label=_("Age range"),
    )
    country = forms.CharField(
        max_length=2, required=False, label=_("Country (ISO code, such as FR)")
    )
    region = TextField(max_length=100, required=False, label=_("Region"))
    languages = TextField(
        max_length=200,
        required=False,
        label=_("Languages you live in"),
        help_text=_("Language tags separated by commas, such as fr, en."),
    )
    profession = TextField(max_length=100, required=False, label=_("Profession"))
    field = forms.ChoiceField(
        choices=[("", _("Not given")), *vocab.Field.choices],
        required=False,
        label=_("Field"),
    )
    field_note = TextField(
        max_length=200, required=False, label=_("Field, in your words")
    )
    organization = TextField(max_length=200, required=False, label=_("Organization"))
    organization_type = forms.ChoiceField(
        choices=[("", _("Not given")), *vocab.OrganizationType.choices],
        required=False,
        label=_("Type of organization"),
    )
    organization_type_note = TextField(
        max_length=200, required=False, label=_("Type of organization, in your words")
    )
    relationship_to_ai = forms.MultipleChoiceField(
        choices=vocab.RelationshipToAI.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_("Your relationship to AI"),
    )
    relationship_to_ai_note = TextField(
        max_length=200, required=False, label=_("Relationship to AI, in your words")
    )
    link = forms.URLField(max_length=2000, required=False, label=_("Link"))

    authorship_category = forms.ChoiceField(
        choices=vocab.AuthorshipCategory.choices,
        widget=forms.RadioSelect,
        initial=vocab.AuthorshipCategory.NONE,
        label=_("Did you use AI to write this testimony?"),
    )
    provider = TextField(max_length=100, required=False, label=_("AI provider"))
    product = TextField(max_length=100, required=False, label=_("AI product"))
    model = TextField(max_length=100, required=False, label=_("Model"))
    model_version = TextField(max_length=100, required=False, label=_("Model version"))
    mode_or_setting = TextField(
        max_length=200,
        required=False,
        label=_("Mode or setting, such as an effort level"),
    )
    inputs = TextField(
        multiline=True,
        max_length=1000,
        required=False,
        widget=forms.Textarea,
        label=_("What information the AI system received"),
    )
    workflow = TextField(
        multiline=True,
        max_length=1000,
        required=False,
        widget=forms.Textarea,
        label=_("Prompts or workflow"),
    )
    changes_after = TextField(
        multiline=True,
        max_length=1000,
        required=False,
        widget=forms.Textarea,
        label=_("What you changed afterwards"),
    )
    comment = TextField(
        multiline=True,
        max_length=1000,
        required=False,
        widget=forms.Textarea,
        label=_("Other comment on the AI use"),
    )

    ai_use_frequency = forms.ChoiceField(
        choices=[("", _("Not given")), *vocab.AIUseFrequency.choices],
        required=False,
        label=_("How often you use AI"),
    )
    tools_used = TextField(
        multiline=True,
        max_length=2000,
        required=False,
        widget=forms.Textarea,
        label=_("Tools you use"),
        help_text=_("One per line."),
    )
    attitude = forms.ChoiceField(
        choices=[("", _("Not given")), *vocab.Attitude.choices],
        required=False,
        label=_("Your attitude towards AI"),
    )
    attitude_note = TextField(
        max_length=200, required=False, label=_("Attitude, in your words")
    )
    prediction = TextField(
        multiline=True,
        max_length=2000,
        required=False,
        widget=forms.Textarea,
        label=_("A prediction to leave on record"),
    )
    prediction_horizon = forms.IntegerField(
        min_value=2026,
        max_value=2200,
        required=False,
        label=_("Year the prediction is for"),
    )

    def clean_languages(self):
        return _tag_list(self.cleaned_data["languages"], _("language tags"))

    def clean_tools_used(self):
        tools = [line.strip() for line in self.cleaned_data["tools_used"].splitlines()]
        tools = [tool for tool in tools if tool]
        if any(len(tool) > 100 for tool in tools):
            raise ValidationError(_("Each tool is at most 100 characters."))
        return tools

    def clean_country(self):
        country = self.cleaned_data["country"].strip().upper()
        if country and not re.fullmatch(r"[A-Z]{2}", country):
            raise ValidationError(_("Use a two-letter country code, such as FR."))
        return country

    def clean_link(self):
        link = self.cleaned_data["link"]
        if link and not link.startswith(ALLOWED_LINK_SCHEMES):
            raise ValidationError(
                _("Use a web address starting with http:// or https://.")
            )
        return link

    def clean(self):
        cleaned = super().clean()
        identity = cleaned.get("identity_mode")
        if identity == vocab.IdentityMode.ANONYMOUS:
            if cleaned.get("display_name"):
                self.add_error(
                    "display_name", _("Anonymous testimonies have no display name.")
                )
        elif identity and not cleaned.get("display_name"):
            self.add_error(
                "display_name", _("Give a display name, or publish anonymously.")
            )

        if cleaned.get("language"):
            cleaned["language"] = canonical_language(cleaned["language"])

        category = cleaned.get("authorship_category")
        ai_fields = [
            "provider",
            "product",
            "model",
            "model_version",
            "mode_or_setting",
            "inputs",
            "workflow",
        ]
        if category in (
            vocab.AuthorshipCategory.NONE,
            vocab.AuthorshipCategory.UNDISCLOSED,
        ):
            for name in ai_fields:
                if cleaned.get(name):
                    self.add_error(
                        name,
                        _("Leave this empty unless you say that AI was used."),
                    )

        if cleaned.get("prediction_horizon") and not cleaned.get("prediction"):
            self.add_error("prediction", _("Write the prediction the year refers to."))
        return cleaned


def _tag_list(value, label):
    tags = []
    for raw in value.split(","):
        tag = raw.strip()
        if not tag:
            continue
        if not LANGUAGE_TAG.match(tag):
            raise ValidationError(_("Use %(label)s such as fr, en.") % {"label": label})
        canonical = canonical_language(tag)
        if canonical not in tags:
            tags.append(canonical)
    return tags


class SubmissionForm(forms.Form):
    declared_age_band = forms.ChoiceField(
        choices=vocab.DeclaredAgeBand.choices,
        widget=forms.RadioSelect,
        label=_("Are you 16 or over?"),
        help_text=_("We ask only this, not your exact age."),
    )
    publication_statement = forms.BooleanField(
        required=True,
        label=_(
            "Publish my testimony in the guestbook, including anything personal it reveals about me."
        ),
    )


class ParentalEmailForm(forms.Form):
    parent_email = forms.EmailField(
        max_length=254,
        label=_("Email address of your parent or legal guardian"),
    )


class ParentalConfirmForm(forms.Form):
    parental_statement = forms.BooleanField(
        required=True,
        label=_(
            "I am this young person's parent or legal guardian, and I consent to their "
            "testimony being published as described."
        ),
    )
