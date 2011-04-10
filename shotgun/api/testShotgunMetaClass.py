from shotgun.api.shotgun_api3 import Shotgun  as __Shotgun
from redis import Redis as __Redis

class Redis( __Redis ):
	def __init__( self, host='localhost' ):
		super( Redis, self ).__init__( host )


class ShotgunConnection( type ):
	def __new__( cls, name, bases, attrs ):
		# We look for the attribute 'connectAs' in the list of attributes
		# that we recieve. The base for the new class is then set 
		# dependant on the value of the connectAs attribute.
		# 
		# __shotgun.find() becomes Shotgun.sg_find() in our new class.
		
		
		return super( ShotgunConnection, cls ).__new__( cls, name, bases, newattrs )
		
		
class Shotgun( __Shotgun, Redis ):
	__metaclass__ = ShotgunConnection
	
	def __init__( self, script, connectAs='Redis' ):
		super( Shotgun, self ).__init__( url, scriptname, key )
		
		
		
sg = Shotgun( 'NewVersion' )