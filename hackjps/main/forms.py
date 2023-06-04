from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LandingForm(forms.Form):
    school = forms.CharField(label="School", max_length=100)
    school = forms.CharField(label="Route", max_length=100)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput()
    )
    
    OCCUPATIONS = (
        ('student', 'STUDENT'),
        ('driver', 'DRIVER'),
        ('teacher', 'TEACHER'),
        ('principal', 'PRINCIPAL'),
    )
    occupations = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=OCCUPATIONS
    )

    # Add the stop field for students
    stop_choices = [
        ('Grove Ave and Wintergreen Ave. West', 'Grove Ave and Wintergreen Ave. West'),
        ('Rollingbrook Dr. & Lyle Place', 'Rollingbrook Dr. & Lyle Place'),
        ('Rahway Rd & Madaline Dr.', 'Rahway Rd & Madaline Dr.'),
        ('Rahway Rd & MaryEllen Dr.', 'Rahway Rd & MaryEllen Dr.'),
        ('Old Raritan Road & Webb St.', 'Old Raritan Road & Webb St.'),
        ('Old Raritan Rd & Wright St.', 'Old Raritan Rd & Wright St.'),
        ('Old Raritan Rd and King St.', 'Old Raritan Rd and King St.'),
        ('Old Raritan Rd & Inman Ave.', 'Old Raritan Rd & Inman Ave.'),
        ('Tingley Ln & Inman Ave.', 'Tingley Ln & Inman Ave.'),
        ('Tingley Ln & Timber Oaks Rd.', 'Tingley Ln & Timber Oaks Rd.'),
        ('Woodland Ave & Fairview Ave.', 'Woodland Ave & Fairview Ave.'),
    ]
    stop = forms.ChoiceField(choices=stop_choices, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "occupations", "stop")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       




class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 4px;'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 4px;'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data


