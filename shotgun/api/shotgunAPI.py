from shotgun.api.shotgun_api3 import Shotgun  as _Shotgun
from shotgun.api.redis_api3 import Redis  as _Redis
from shotgun.api.redis_api3 import ConnectionError
import shotgun.api.keys

import pickle

def getURL():
	return shotgun.api.keys.url
	
def getKey( index ):
	return shotgun.api.keys.keys[index]

class Shotgun( _Shotgun, _Redis ):
	"""
	Abstraction around the main shotgun api. Purpose being to allow for something to be put inbetween
	such as a datastore or other caching mechanism.
	"""
	
	#need to retrieve the url and api key. 
	
	# v1.0 
	def __init__( self, url='', scriptname='', key='', connection='cached' ):
		# Initialises an intermediate object which masquerades access to either of the
		# parent class types. 
		#
		# Connection can be:
		#
		# 'direct' - do not route though cache
		# 'cached' - attempt to access cache first, then shotgun server if not data found
		# 'local' - only access the cache, return None if no data found.
		#
		# If no script name has been provided then access will default to the
		# local redis cache. If a call is made to a key which does not exist
		# then the result will be returned as a None without an attempt to 
		# query the shotgun server. 
		# If a scriptname is provided then local redis access is set as the default
		# pulling data from the fast storage channel. Should the key requested 
		# not exist due to never being pulled accross or expriation since the last 
		# request then the redis object will query the shotgun server, return 
		# result and store it it in the cache.
		
		self.sg_url = url
		self.sg_key = key
		self.sg_script = scriptname
		
		if scriptname:
			self.connect_type = connection
		else:
			self.connect_type = 'local'
		
				
		if self.connect_type == 'direct':
			# to be used only by applications which require accurate updates from the shotgun
			# server. Should be sparingly used.
			
			_Shotgun.__init__( self, self.sg_url, self.sg_script, self.sg_key )
			print "Info: Direct connection to Shotgun initiated"
			
		elif self.connect_type == 'cached':
			# default mode of operation. To query against the local cache first before calling
			# shotgun if no recent data is present.
			
			_Shotgun.__init__( self, self.sg_url, self.sg_script, self.sg_key )
			
			_Redis.__init__( self, 'localhost', db=1 )
			print "Info: Cached connection to Shotgun initiated"
			
		elif self.connect_type == 'local':
			# a high speed, low accuracy option. typically used by applications which request
			# data which is infrequently updated such as for a list of file types or where the
			# data is internally generated and not stored on the shotgun db.
			
			_Redis.__init__( self, 'localhost', db=1 )			
			print "Info: Local cache connection initiated"
			
	# v2.0 - Impliments controls over read functions from shotgun.

	##################################
	# Find functions - external api is 'find'
	# Hash is based on python hash builtin. 
	##################################

	def find( self, *args, **kwargs ):
		"""controls access to implimentation specific versions of find. such as find_cache, find_direct"""
		# Find which attempts to read from local network cache before
		# falling back onto the shotgun server if no data can be found.
		# Any responses from shotgun are stored into the network cache
		# to reduce latency on subsequent calls.

		if self.connect_type == 'direct': 
			return self.direct_find( *args, **kwargs )
			
		elif self.connect_type == 'local': 
			return self.cache_only_find( *args, **kwargs )
			
		else: 
			return self.cached_find( *args, **kwargs )

	def direct_find( self, *args, **kwargs ):
		"""Direct access to shotgun."""
		
		result = super( Shotgun, self ).find( *args, **kwargs )
		
		return result

	def cached_find( self, *args, **kwargs ):
		"""Checks in cache for the query data and makes a request to shotgun if not present"""

		try:
			query = list( args )						# start off by copying the args list 
			query.append( kwargs )					# and then add on any keyword args
			query_key = hash( pickle.dumps( query ) ) 	# a simple hash for indexing
			
			if self.exists( query_key ):
				return pickle.loads( self.get( query_key ) )
			else:
				result = super( Shotgun, self ).find( *args, **kwargs )
				self.set( query_key , pickle.dumps(result, 2) )
				
				self.expire( query_key , 600 ) 			# 10 minute expiration
				return result
		
		except ConnectionError:
			print "Warning: Cannot connect to local cache, attempting direct connection"
			self.connect_type = 'direct'
			return self.find( *args, **kwargs )
		
	def cache_only_find( self, *args, **kwargs ):
		"""Checks in cache for the query data and makes a request to shotgun if not present"""
		
		try:
			query = list( args )						# start off by copying the args list 
			query.append( kwargs )					# and then add on any keyword args
			query_key = hash( pickle.dumps( query ) ) 	# a simple hash for indexing
			
			if self.exists( query_key ):
				return pickle.loads( self.get( query_key ) )
			else:
				return []
		except ConnectionError:
			print "Warning: Cannot connect to local cache"
			return []

	def find_one( self, *args, **kwargs ):
		# Find which attempts to read from local network cache before
		# falling back onto the shotgun server if no data can be found.
		# Any responses from shotgun are stored into the network cache
		# to reduce latency on subsequent calls.
		
		return super( Shotgun, self ).find_one( *args, **kwargs )
		
	def schema_read( self ):
		return super( Shotgun, self ).schema_read()
		
	def schema_field_read( self, field  ):
		return super( Shotgun, self ).schema_field_read( field )
	
	def schema_entity_read( self ):
		return super( Shotgun, self ).schema_entity_read( )























