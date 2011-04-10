import re

import shotgun.api.shotgunAPI as sgAPI

sg = sgAPI.Shotgun( 'https://baseblack.shotgunstudio.com', 
				'NewVersion', 
				'df403e9631a26b4c018be400ba048e8bc404b845', 
				connection='local' ) #direct/cached/local

fields = ['id','code','project']
filters = [[ 'project','is', {'type':'Project', 'id':74 } ]]

results =  sg.find( 'Version', filters, fields )
print  '#results: ', len(results)


#result =  sg.find( 'Version', filters, fields )
#print  '#results: ', len(result)
#print "RESULT: ", result[0]

shots = []
for result in results:
	shots.append( result['code'] )
	
print shots
print ">>"
print [ shot for shot in shots if re.match( '.*gl.*', shot) ]
