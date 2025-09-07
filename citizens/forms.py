from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from issues.models import UserProfile, Issue, Category

class CitizenRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.CharField(initial='Citizen', widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Check if profile already exists (from signal)
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user, role='Citizen')
        return user

class IssueReportForm(forms.ModelForm):
    # GPS location fields
    use_current_location = forms.BooleanField(required=False, initial=True, label="Use my current location")
    manual_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Or enter address manually'}))

    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', 'priority', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'priority': forms.Select(attrs={'class': 'priority-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field required
        self.fields['image'].required = True
        self.fields['image'].help_text = "Please upload an image of the issue (required)"

    def clean(self):
        cleaned_data = super().clean()
        use_current_location = cleaned_data.get('use_current_location')
        manual_address = cleaned_data.get('manual_address')

        # Validate that either GPS or manual address is provided
        if not use_current_location and not manual_address:
            raise forms.ValidationError("Please either use your current location or enter an address manually.")

        return cleaned_data