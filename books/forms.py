from django import forms


class ReviewForm(forms.Form):
    review = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder': 'Write short description about what you think about this book'}),
    )
