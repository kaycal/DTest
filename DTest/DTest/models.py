from django.db import models

###################
# Class - Client  #
###################

class Client(models.Model):
    """Instances represent a peer entity in the torrent swarm.
       These should be very malleable; for the time being, until
       a better solution is provided. Note that it is one Client
       per torrent, not one client with many torrents.
       >>> c = Client.create(request)
       >>> if c.is_valid() c.save()
    """
    
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    torrent = models.ForeignKey(Torrent)

    state_choices = (
        ('seeding','Seeding'),
        ('leeching','Leeching'),
        ('started','Initializing'),
        ('inactive','Inactive'),
    )



    state = models.CharField(max_length=12,choices=state_choices, default='inactive')
    
    @classmethod
    def create(request):
        c = Client(name="Test",ip="192.168.1.1",port=2489)
        return c

    def __unicode__(self):
        return self.name

    def setState(self, state):
        options = {"seeding":self.__startSeeding__,
                   "started":self.__initialize__,
                   "inactive":self.__quit__
                  }
        self.state = options[state.lower()]()
        

    def __startSeeding__(self): # Little more than a "flag" for identifying prime peers
        return "Seeding"

    def __initialize__(self): # Add / create client
        return "Starting"

    def __quit__(self): # Attempt to remove the client entity
        self.delete()
        return "Inactive"
            

class Torrent(models.Model):
    name = models.CharField(max_length=200,unique=True)
    info_hash = models.CharField(max_length=20)
    size = models.BigIntegerField()

    @classmethod
    def create(info_hash=None):
        pass
        # return Torrent.get_or_create()
    
    def __unicode__(self):
        return self.name




#####################
# Utility functions #
#####################

def getTorrent(hash):
    for t in Torrent.objects.all():
        if hash.lower() == t.info_hash.lower():
            # d,k = **t # Check this!!!
            peers = {}
            return {"name":t.name,
                    "info_hash":t.info_hash,
                    "size":t.size,
                    "peers":t.client_set.all(),
                    "torrent":t
                   }
#    print "Suspected problem spot"
    raise Exception("Torrent not found:\ninfo_hash: {}\npassedhash: {}".format(hash.encode('utf-8')
                                                                                ,t.info_hash))

#############
# Database read/write
#############

def handleClient(info=None,req=None,torrent=None):
    try:
        # Try to fetch client
        c, created = Client.objects.get_or_create(name=info[u'peer_id'],
                                                          ip=req.META["REMOTE_ADDR"],
                                                          port=int(info[u'port'][0]),
                                                          )
        c.setState(info[u'event'][0])
        # Later; check params for downloaded / left, try to use peers w/ less
        # data remaining to pass to lacking peers, when seeders are unavailable
        #
        # Save client changes
    except Exception as e:
        print e, "<--Here?"
    print "Probs not here."
