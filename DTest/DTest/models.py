from django.db import models

def getTorrent(hash):
    for t in Torrent.objects.all():
        if hash.lower() == t.info_hash.lower():
            # d,k = **t # Check this!!!
            peers = {}
            return {"name":t.name,
                    "info_hash":t.info_hash,
                    "size":t.size,
                    "peers":peers,
                    "torrent":t
                   }
#    print "Suspected problem spot"
    raise Exception("Torrent not found: - info_hash: {} - passedhash: {}".format(hash.encode('utf-8')
                                                                                ,t.info_hash))



class Client(models.Model):
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()

    state_choices = (
        ('seeding','Seeding'),
        ('leeching','Leeching'),
        ('started','Initializing'),
        ('inactive','Inactive'),
    )



    state = models.CharField(max_length=12,choices=state_choices, default='inactive')

    def __unicode__(self):
        return self.name

    def setState(self, state):
        options = {"seeding":self.__startSeeding__,
                   "started":self.__initialize__,
                   "inactive":self.__quit__
                  }
        self.state = options[state.lower()]()
        

    def __startSeeding__(self):
        return "Seeding"

    def __initialize__(self):
        return "Starting"

    def __quit__(self):
        return "Inactive"
            

class Torrent(models.Model):
    name = models.CharField(max_length=200,unique=True)
    info_hash = models.CharField(max_length=20)
    size = models.BigIntegerField()
    peers = models.ManyToManyField(Client)

    def __unicode__(self):
        return self.name

    def getPeers(self):
        p = {}
        for peer in self.peers.all():
            p[peer.name] = peer,(True if self in peer.getSeeds() else False)
        print p





#############
# Utility functions
#############


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
