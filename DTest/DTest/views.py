from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from .forms import UploadTorrentForm
from models import Torrent
import datetime
import torUtils

def front(request):
    return render_to_response('front.html',{'torrents':Torrent.objects.all()})

def upload(request):
    if request.method == 'POST':
        print request.FILES['torrent']
        form = UploadTorrentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_torrent_file(request.FILES['torrent'])
            return HttpResponseRedirect('/')
    else:
        form = UploadTorrentForm()
    return render(request,'upload', {'form': form})

def handle_torrent_file(torrent):
    t = ""
    for chunk in torrent.chunks():
        print chunk
        t = str.join(t,chunk)
    print torUtils.bdecode(t)

def announce(request):
    pass

def scrape(request):
    print torUtils.getParams(request.get_full_path())
