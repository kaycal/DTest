from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from .forms import UploadTorrentForm
import bencode
import models
import datetime
import torUtils

def front(request):
    form = UploadTorrentForm()
    if request.method == 'POST':
        form = UploadTorrentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if handle_upload(request.FILES['torrent']):
                    return render_to_response('front.html',
                                                           {'torrents':models.Torrent.objects.all(),'uploaded':True,'form':form},
                                                           context_instance=RequestContext(request))
            except Exception as e:
                print e
    return render_to_response('front.html',
                                           {'torrents':models.Torrent.objects.all(),'uploaded':False,'form':form},
                                           context_instance=RequestContext(request))

def handle_upload(torrent):
    t = ""
    if torrent.name.split(".")[1].lower() == "torrent":
        t = ""
        for chunk in torrent.chunks():
            t = str.join(t,chunk)
        tr = models.Torrent(**torUtils.getInfo(t,torrent.name.split(".")[0]))
        tr.save()
        return True
    else:
        raise Exception("Not a torrent file.")

def announce(request):
    print torUtils.getParams(request.get_full_path())
    # Match info hash against a particular Torrent
    # Match client against list of known users
    # If announce, take internal action; OH FUCK HERE IS AN ALGORITHM I MUST WRITE :(
    # -- Seeding:
    # -- Leeching:
    # -- Loading:
    # -- Inactive:
    # If no announce, double-check peer connections, and send a new list
    pass

def scrape(request):
    bdT = models.getTorrent(torUtils.getParams(request.get_full_path())['info_hash'][0])
    bd = {
          "files":{
                   bdT["info_hash"]:{
                        "complete":len(bdT["torrent"].peers.all()), # Number of seeders (integer)
                        "downloaded":0, # total number of times the tracker has registered a completion
                        "incomplete":0, # Number of non-seeder peers / leechers (integer)
                        "name":"Blah", # Torrent's internal name, as specified by the "name" file
                       }
                  }
         }
    return HttpResponse(bencode.bencode(bd))
