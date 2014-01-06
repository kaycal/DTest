import binascii
import bencode
import hashlib
import urllib

#############################
# Generic utility functions #
#############################

# TODO
# Clean up a bit, but otherwise ok for now
def getParams(url):
    """getParams(<string>):
        returns a dictionary of an & delimited url, with its respective keys and values
    """
    try:
        params = url.split("?")[1]
    except:
        return {"Fail":"Was the url used malformed?\r\t" + url}
    d = {}
    for k in params.split("&"):
        d[k.split("=")[0]]=k.split("=")[1:]
    return d

# TODO
# Error-checking
def getHash(file): # ex getHash(open("file.torrent").read())
    """Return the info_hash for the particular torrent.
       Should probably take a shot at adding error-checking
       here."""
    hash = bencode.bdecode(file)
    hash = hashlib.sha1(bencode.bencode(hash['info'])).hexdigest()
    return binascii.a2b_hex(hash)

# TODO
# Flesh out the dictionary; this will be sent to clients (likely)
def getInfo(file,name):
    return {"name":name,
            "info_hash":urllib.quote(getHash(file)),
            "size":1234,
            }
