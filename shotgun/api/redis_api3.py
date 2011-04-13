#import redis
from redis import Redis, ConnectionError

__version__ = "3.0.6" #to match shotgun api.

__all__ = [ 'Redis', 'ConnectionError' ]

"""
Python Shotgun API library.
"""

#class Redis( redis.Redis ):
	# Used to split up requests into batches of records_per_page when doing requests.  this helps speed tremendously
	# when getting lots of results back.  doesn't affect the interface of the api at all (you always get the full set
	# of results back as one array) but just how the client class communicates with the server.
#	expire_mins = 60
	
#	def __init__( self , *args, **kwargs ):
"""
Initialize Shotgun. The default host and port are 'localhost', 6379
and are defined the arguments to the redis.Redis module.
"""
#		super(Redis, self).__init__( args, kwargs )
		
		