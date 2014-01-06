from django.db import models

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
    
    def getPeer(name=None):
        if name is not None:
            return this.client_set.filter(client_name__startswith=name)
        else:
            return this.client_set.all()

    @classmethod
    def create(info_hash=None,name=None):
        # Attempt to create and save torrent
        # If pass, return torrent
        # If fail, raise exception
        pass
    
    @classmethod
    def getTorrent(info_hash=None,name=None):
        for t in Torrent.objects.all():
            if info_hash.lower() == t.info_hash.lower() or name.lower() == t.name.lower():
                return {"name":t.name,
                        "info_hash":t.info_hash,
                        "size":t.size,
                        "torrent":t
                       }
    #    print "Suspected problem spot"
        raise Exception("Torrent not found:\ninfo_hash: {}\npassedhash: {}".format(hash.encode('utf-8')
                                                                                    ,t.info_hash))
    
    def __unicode__(self):
        return self.name


##################
# Class - Client #
##################

class Client(models.Model):
    """Instances represent a peer entity in the torrent swarm.
       These should be very malleable; for the time being, until
       a better solution is provided. Note that it is one Client
       per torrent, not one client with many torrents.
       >>> c = Client.create(request)
       >>> if c.is_valid() c.save()
    """
    
    name = models.CharField(max_length=20, unique=True)
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
    def create(n = None, i = None, p = None, ih = None):
        try:
            t = Torrent.getTorrent(info_hash=ih)["torrent"]
            c = Client(name=n,ip=i,port=p, torrent=t)
            c.save()
        except NameError:
            print "One or more variables may not have been initialized."
        except Exception as e:
            print e
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
