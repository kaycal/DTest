
####
# torrent-protocol
########

class torUtils:

	# Generic bencoder.
	def bencode(self, o):
		string = ""

		if type(o) is list:
			string = self.__bencode_list(o)
		elif type(o) is dict:
			string = self.__bencode_dict(o)
		elif type(o) is str:
			string = self.__bencode_str(o)
		elif type(o) is int:
			string = self.__bencode_int(o)
		else:
			raise ValueError('Not a list, dict, str, or int')
		return string

	def __bencode_list(self, o):
		temp = "l"
		for i in o:
			temp += self.bencode(i)
		temp += "e"
		return temp

	def __bencode_dict(self, o):
		temp = "d"
		for k in o.keys():
			temp += self.bencode(k)
			temp += self.bencode(o[k]) # hahaha
		temp += "e"
		return temp

	def __bencode_str(self, o):
		temp = str(len(o)) + ":"
		temp += o
		return temp

	def __bencode_int(self, o):
		temp = "i" + str(o) + "e"
		return temp


	# Generic bdecoder.

#############################
# Generic utility functions #
#############################

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
