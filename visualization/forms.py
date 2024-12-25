from django import forms

class CharacterSearchForm(forms.Form):
    query = forms.CharField(
        label='搜索人物',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '输入人物名称进行搜索...'
        })
    )
