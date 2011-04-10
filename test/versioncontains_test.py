import re
import pprint

import shotgun.api.shotgunAPI as sgAPI

sg = sgAPI.Shotgun( 'https://baseblack.shotgunstudio.com', 
				'NewVersion', 
				'df403e9631a26b4c018be400ba048e8bc404b845', 
				connection='cached' ) #direct/cached/local

sg_version_numbers = set()

fields = ['id','code','sg_version_number','project']
filters = [[ 'project','is', {'type':'Project', 'id':74 } ],['code','starts_with', '251_gl_090_postfix_v' ]]

results =  sg.find( 'Version', filters, fields )

          jQuery( function() {

for result in results:
	sg_version_numbers.add( result['sg_version_number'] )

pprint.pprint( results )
pprint.pprint( sg_version_numbers )
