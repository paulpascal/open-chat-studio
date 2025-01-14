from django import forms
from django.utils.translation import gettext_lazy as _


class ProviderTypeConfigForm(forms.Form):
    def save(self, instance):
        instance.config = self.cleaned_data
        return instance


class ObfuscatingMixin:
    """Mixin that obfuscate configured field values for display."""

    obfuscate_fields = []

    def __init__(self, initial=None, *args, **kwargs):
        self.initial_raw = initial
        if initial:
            initial = initial.copy()
            for field in self.obfuscate_fields:
                initial[field] = obfuscate_value(initial.get(field, ""))
        super().__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.initial:
            return cleaned_data

        for field in self.obfuscate_fields:
            initial = self.initial.get(field)
            new = obfuscate_value(self.cleaned_data.get(field))
            if new == initial:
                cleaned_data[field] = self.initial_raw.get(field)

        return cleaned_data


class OpenAIConfigForm(ObfuscatingMixin, ProviderTypeConfigForm):
    obfuscate_fields = ["openai_api_key"]

    openai_api_key = forms.CharField(label=_("API Key"))
    openai_api_base = forms.URLField(
        label="API Base URL",
        required=False,
        help_text="Base URL path for API requests. Leave blank for the default API endpoint.",
    )
    openai_organization = forms.CharField(
        label="Organization ID",
        required=False,
        help_text=_(
            "This allows you to specify which OpenAI organization to use for your API requests if you belong"
            " to multiple organizations. It is not required if you only belong to"
            " one organization or want to use your default organization."
        ),
    )


class AzureOpenAIConfigForm(ObfuscatingMixin, ProviderTypeConfigForm):
    obfuscate_fields = ["openai_api_key"]

    openai_api_key = forms.CharField(label=_("Azure API Key"))
    openai_api_base = forms.URLField(
        label="API URL",
        help_text="Base URL path for API requests e.g. 'https://<your-endpoint>.openai.azure.com/'",
    )
    openai_api_version = forms.CharField(
        label="API Version",
        help_text="API Version e.g. '2023-05-15'",
    )


def obfuscate_value(value):
    if value and isinstance(value, str):
        return value[:4] + "*" * (len(value) - 4)
    return value


class AWSVoiceConfigForm(ObfuscatingMixin, ProviderTypeConfigForm):
    obfuscate_fields = ["aws_secret_access_key"]

    aws_access_key_id = forms.CharField(label=_("Access Key ID"))
    aws_secret_access_key = forms.CharField(label=_("Secret Access Key"))
    aws_region = forms.CharField(label=_("Region"))


class AzureVoiceConfigForm(ObfuscatingMixin, ProviderTypeConfigForm):
    obfuscate_fields = ["azure_subscription_key"]

    azure_subscription_key = forms.CharField(label=_("Subscription Key"))
    azure_region = forms.CharField(label=_("Region"))
