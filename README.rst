A super simple local cache layer wrapping around the shotgun python api https://github.com/shotgunsoftware/python-api. 

When working with the Shotgun hosted solution we sometimes don't want to be make duplicate calls to the servers for data which we know is unlikely to have changed since the last call was made.

Examples of how we've used this to reduce the amount we pull from the servers are:

+ Version data , such as the locations of locally stored quicktimes and their thumbnails. 
+ Sequence/Shot data , irregularly updated and safe to cache.
+ Configuration information used to generate automated assets.

A Simple Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since no documentation is complete without some kind of documentation to demonstrate how it works here is a simple cached find::

	from shotgun.api import shotgunAPI as sgAPI

	SG_URL='https://foo.shotgun.com/'
	SG_SCRIPT='shotgun-redis'
	SG_KEY='SECRETKEY'

	projectname = 'redisproj'

	sg = sgAPI.Shotgun( SG_URL, SG_SCRIPT, SG_KEY, connection='cached' ) # possible choices are direct/cached/local

	projectID = sg.find('Project', [['name','is', projectname ]], ['id'] )[0]

The first time the find method is called the cache is checked for the presense of the arguments pickled into a hashed string. If no key is found in the cache a call to the 'real' find method is made and the result stored into the cache.

By default the cache stores data for around 10mins or so at the moment. I'll see about exposing that as an option per call so that on a cached request you can set how long to maintian the data cache for.

Types of Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

direct
	The whole caching mechanism is shortcircuited and all calls are directed to the 
	shotgun servers.
cached
	The default behaviour, each request is checked in the cache first and only directed
	if it not present.
local
	For if you want to run offline, a check will be made with the cache for data, but if 
	none is found it returns an empty list.

