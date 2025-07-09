from django import forms

class PreSignupform(forms.Form):
    full_name = forms.CharField(max_length=100)
    email_or_phone = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data =  super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

