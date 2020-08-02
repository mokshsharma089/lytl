from django import forms
from.validators import validate_url,validate_dot_com


class SubmitUrlForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(),max_length = 600,label="Submit long URL")
    shortcode=forms.CharField(required=False, widget=forms.TextInput(),label="Submit shortcode")