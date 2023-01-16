from django import forms


class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea )

    def get_error_messages(self):
        errors = {'review': ''}
        return errors



