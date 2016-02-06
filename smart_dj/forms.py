from django import forms

class PreferencesForm(form.Form):
    song_title = forms.CharField(max_length=30,
                                 label='',
                                 widget=forms.TextInput(attrs={'placeholder': 'Song Title', 'autocomplete':'off'}))
    artist_name = forms.CharField(max_length=60,
                                  label='',
                                  widget=forms.TextInput(attrs={'placeholder': 'Artist Name', 'autocomplete':'off'}))

class LikesForm(PreferencesForm):
    pass

class DislikesForm(PreferencesForm):
    pass
