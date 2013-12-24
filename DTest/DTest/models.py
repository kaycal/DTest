from django.db import models

def getTorrent(hash):
    for t in Torrent.objects.all():
        if hash == t.info_hash:
            # d,k = **t # Check this!!!
            peers = {}
            for p in t.peers.all(): # Django has a way of doing this funny, check inside
                peers[p.__unicode__()] = p
            return {"name":t.name,
                    "info_hash":t.info_hash,
                    "size":t.size,
                    "peers":peers,
                    "torrent":t
                   }
    return "Nope :("



class Client(models.Model):
    name = models.CharField(max_length=20,unique=True)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()

    state_choices = (
        ('SEEDING','Seeding'),
        ('LEECHING','Leeching'),
        ('LOADING','Initializing'),
        ('INACTIVE','Inactive'),
    )

    seeding = []

    state = models.CharField(max_length=12,choices=state_choices, default='INACTIVE')

    def __unicode__(self):
        return self.name

    def getState(self):
        return self.state

    def getSeeds(self):
        seeds = []
        for s in seeding:
            seeds.add(getTorrent(s)["torrent"])
            

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
