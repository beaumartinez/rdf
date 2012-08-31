from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import ModelForm
from floppyforms.widgets import CheckboxInput, NumberInput

from rdf.models import Settings
from rdf.constants import MAX_FREQUENCY, MIN_FREQUENCY

class SettingsForm(ModelForm):

    class Meta(object):

        fields = (
            'frequency',
            'paused',
        )

        model = Settings

        widgets = {
            'frequency': NumberInput(attrs={'max': MAX_FREQUENCY, 'min': MIN_FREQUENCY}),
            'paused': CheckboxInput,
        }

    helper = FormHelper()
    helper.layout = Layout(
        'frequency',
        'paused',

        FormActions(
            Submit('update', 'Update', css_class='btn-primary'),
        )
    )
