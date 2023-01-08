from django import forms

class ReviewForm(forms.Form):
    user_score = forms.IntegerField()