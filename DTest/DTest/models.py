from django.db import models

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

    state = models.CharField(max_length=12,choices=state_choices, default='INACTIVE')

    def __unicode__(self):
        return self.name

    def getState(self):
        return self.state

class Torrent(models.Model):
    name = models.CharField(max_length=200,unique=True)
    info_hash = models.CharField(max_length=20)
    size = models.BigIntegerField()
    peers = models.ManyToManyField(Client)

    def __unicode__(self):
        return self.name
