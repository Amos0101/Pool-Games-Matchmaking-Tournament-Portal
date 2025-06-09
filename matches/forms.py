from django import forms
from .models import Match, Venue
from django.contrib.auth import get_user_model

User = get_user_model()

class MatchCreateForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['opponent', 'venue', 'match_date', 'match_time', 'bid_amount']
        widgets = {
            'opponent': forms.Select(attrs={'class': 'form-control'}),
            'venue': forms.Select(attrs={'class': 'form-control'}),
            'match_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'match_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'bid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        
        if current_user:
            # Exclude current user from opponent choices
            self.fields['opponent'].queryset = User.objects.filter(
                user_type='player'
            ).exclude(id=current_user.id)
