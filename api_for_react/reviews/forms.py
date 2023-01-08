from django import forms

class ReviewForm(forms.Form):
    score = forms.IntegerField()