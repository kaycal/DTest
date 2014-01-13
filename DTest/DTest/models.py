from django.db import models, IntegrityError
import hashlib

####################
# Class - Torrent  #
####################

# TODO
# 
class Torrent(models.Model):
    """Notes and things
    """
    
    name = models.CharField(max_length=200,unique=True)
    info_hash = models.CharField(max_length=20,unique=True)
    size = models.BigIntegerField()
    
    def getPeer(self, name=None, addr=None, seeding=False):
        if name is not None: # Partial matching; TODO full searching
            res = self.client_set.filter(name__startswith=name)
        elif addr is not None:
            res = self.client_set.filter(ip__exact=addr)
        elif seeding is True:
            res = self.client_set.filter(state__exact='seeding')
        else:
            res = self.client_set.all()
        print res
        return res
        
    def __unicode__(self):
        return self.name

    # Class methods
    @staticmethod
    def create(name,info_hash,size):
        try:
            t = Torrent(name=name,info_hash=info_hash,size=size)
            t.save()
            return t
        except IntegrityError:
            raise Exception("Torrent already exists.")
        except Error as e:
            raise Exception(e)
    
    @staticmethod
    def getTorrent(info_hash):
        for t in Torrent.objects.all():
            if info_hash.lower() == t.info_hash.lower():
                return {"name":t.name,
                        "info_hash":t.info_hash,
                        "size":t.size,
                        "torrent":t
                       }
        # Throw a torrent-not-found exception?
        raise Exception("Torrent not found")


##################
# Class - Client #
##################

# TODO
# Hella needs cleaning up
class Client(models.Model):
    """Instances represent a peer entity in the torrent swarm.
       These should be very malleable; for the time being, until
       a better solution is provided. Note that it is one Client
       per torrent, not one client with many torrents.
       >>> c = Client.create(request)
       >>> if c.is_valid() c.save()
    """
    
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(unique=True)
    port = models.IntegerField()
    torrent = models.ForeignKey(Torrent)

    state_choices = (
        ('seeding','seeding'),
        ('leeching','leeching'),
        ('started','initializing'),
        ('inactive','inactive'),
        ('interval','interval'),
    )



    state = models.CharField(max_length=12,choices=state_choices, default='inactive')
    
    @staticmethod
    def get(n = None, i = None, p = None, ih = None, evt = None):
        try:
            t = Torrent.getTorrent(info_hash=ih)["torrent"]
            c,created = Client.objects.get_or_create(name=n[0].encode("utf-8"),ip=i[0].encode("utf-8"),
                                                     port=int(p[0]), torrent=t)
            c.update(evt[0])
            c.save() #<-- This will probs return an error on __quit__. Let's find out.
            return c
        except NameError:
            print "One or more variables may not have been initialized."
        except Exception as e:
            print e, "Client.get() exception"
        raise Exception("Wat")

    def __unicode__(self):
        return self.name

    def update(self, state):
        options = {"seeding":self.__startSeeding__,
                   "started":self.__initialize__,
                   "inactive":self.__quit__,
                   "":self.__interval__
                  }
        self.state = options[state]()
        

    def __startSeeding__(self): # Little more than a "flag" for identifying prime peers
        return "seeding"

    def __initialize__(self): # Client already created upwards a bit
        return "starting"

    def __quit__(self): # Attempt to remove the client entity
        self.delete()
        return

    def __interval__(self):
        return "interval"
