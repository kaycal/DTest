from django import forms

class UploadTorrentForm(forms.Form):
    title = forms.CharField(max_length=200)
    torrent = forms.FileField()
