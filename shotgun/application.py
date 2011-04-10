import shotgun.api.shotgunAPI as shotgunAPI

sgInstance = None

def newShotgunConnection( scriptkey=None, conn='cached' ):
	global sgInstance
	
	if not sgInstance:
		sgInstance = shotgunAPI.Shotgun( scriptkey, conn )

	return sgInstance
	
##########################################################
#
# Playlist Entity type functions
#
##########################################################	
	
def getVersionsInPlaylist( sg, playlist_code ):
	fields = ( [ 'id','entity','code','user','description','project','sg_path_to_frames','sg_version_number' ] )
	filters = [[  'playlists', 'name_contains', playlist_code   ]]

	versions = sg.find( 'Version', filters, fields )
	return versions
		
def getRecentPlaylists( sg, sg_type, period, _at ):
	fields = ['id','code','created_at','updated_at','sg_type']
	filters = [ 
			[ 'sg_type','is', sg_type ], 
			[ 'project','is', {'type':'Project', 'id':self.project_id } ],
			[ _at , 'in_last', period[0], period[1] ] 
		]
	playlists = sg.find( "Playlist", filters, fields )
	
	return playlists
	
def getRecentUpdatedPlaylists( sg, sg_type, period ):
	getRecentPlaylists( sg_type, period, 'updated_at' )
	
	return playlists
	
def getRecentCreatedPlaylists( sg, sg_type, period ):
	getRecentPlaylists( sg, sg_type, period, 'created_at' )
	
	return playlists
	
##########################################################
#
# Version Entity type functions
#
##########################################################
	
def getVersion( sg, version_code ):
	fields = ( [ 'id','entity','code','user','description','project','sg_path_to_frames','sg_version_number' ] )
	filters = [[  'code', 'is', version_code   ]]

	return sg.find_one( 'Version', filters, fields )	
	
##########################################################
#
# Sequence Entity type functions
#
##########################################################
	
def getSequences( sg, project_id ):
	fields = [ 'id','code','shots' ]
	filters = [ [ 'sg_status_list','is','ip' ],[ 'project','is', {'type':'Project', 'id':project_id } ] ]
	return sg.find( "Sequence", filters, fields )
	
##########################################################
#
# Shot Entity type functions
#
##########################################################
	
def getShotStatus( sg, shot_id, projectid ):
	"""Returns the status 'In Progress', 'Omit', 'Final'... etc for a given shot"""
	
	shot_data = getShot( sg, shot_id ) 
	
	return shot_data['sg_master_status']

def getShot( sg, shot_id, status='' ):
	"""Returns a given shot from shotgun. May be filtered by a provided status."""
	
	fields =  ['id','code','sg_master_status']
	filters =  [	[ 'id','is',sho ] ]
	
	if status: filters.append( ['sg_master_status','is',status] )
	
	try:
		result =  sg.find_one( 'Shot', filters, fields )
	except:
		print "Error accessing shot_id '%s'. Please ensure you have entered a valid shot id" % shot_id
		sys.exit(1)
		
	return result
	
##########################################################
#
# Project Entity type functions
#
##########################################################	
	
def getProjects( sg ):
	"""Returns a dict containing the unique id and disk alias for a given project name."""
	
	fields = ['id','name','sg_alias']
	filters = []
	
	project_data = sg.find( "Project", filters, fields )
	
	project_dict = {}
	for project in project_data:
		project_dict[ project['name'] ] = project
	
	return project_dict	
	
def getProject( sg, name ):
	"""Returns a the unique id and disk alias for a given project name."""
	
	fields = ['id','name','sg_alias']
	filters = [['name','is',name]]
	
	try:
		project = sg.find( "Project", filters, fields )
	except:
		print "Error accessing project '%s'. Please ensure you have entered a valid project name" % name
		sys.exit(1)
	
	return project[0]['id'],   project[0]['sg_alias']