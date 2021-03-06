from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
import django.db.utils
from .forms import UploadTorrentForm
import bencode
from models import Torrent, Client
#from models import Utilities as torUtils
import datetime
import torUtils

#
# Human URLS
#

def front(request):
    form = UploadTorrentForm()
    if request.method == 'POST':
        form = UploadTorrentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if handle_upload(request.FILES['torrent']): # <-- Use torrent version
                    return render_to_response('front.html',
                                             {'torrents':models.Torrent.objects.all(),'uploaded':True,'form':form},
                                              context_instance=RequestContext(request))
            except Exception as e:
                print e
    return render_to_response('front.html',
                             {'torrents':Torrent.objects.all(),'uploaded':False,'form':form},
                             context_instance=RequestContext(request))


#
# Torrent URLS
#

def announce(request):
    
    try:
        params = torUtils.getParams(request.get_full_path()) # <-- Add this to models
        ih = params[u'info_hash'][0]
        
        # Match params to grab a specific torrent
        t = Torrent.getTorrent(info_hash=ih)
        
        # Check whether this is a new or returning client
        c = t.getPeer(ip=request.META["REMOTE_ADDR"])
        if c.size == 0:
            c = Client.create(n = params['name'], i = request.META["REMOTE_ADDR"], p = params['port'], ih = params[u'info_hash'][0])
        else:
            # Parse old client
            c = c[0]
        c.update(params["event"])

    except Exception as e:
        print "Torrent not found; ", e
    #     return HttpResponse("Newp!")
    # Match client against list of known users
    # -- Seeding:
    # -- Leeching:
    # -- Loading:
    # -- Inactive:
    # If no announce, double-check peer connections, and send a new list
    return HttpResponse("Fixthis")

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
   
    
#
# Utilities
#

def handle_upload(torrent):
    t = ""
    if torrent.name.split(".")[-1].lower() == "torrent":
        t = ""
        for chunk in torrent.chunks():
            t = str.join(t,chunk)
        try:
            tr = models.Torrent(**torUtils.getInfo(t,torrent.name.split(".")[0]))
            tr.save()
        except Exception as e:
            tr, created = models.Torrent.objects.get_or_create(**torUtils.getInfo(t,torrent.name.split(".")[0]))
            tr.delete()
            tr, created = models.Torrent.objects.get_or_create(**torUtils.getInfo(t,torrent.name.split(".")[0]))
            tr.save()
        return True
        
    else:
        raise Exception("Not a torrent file.")
