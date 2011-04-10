import timeit

setup = """
import shotgun.api.shotgunAPI as sgAPI
sg = sgAPI.Shotgun( 'https://baseblack.shotgunstudio.com', 'OfflineBackup', 'c09d6203d3245ee88e5d1f6bb843e5c71c2b72f0' )
fields = ['id','code','project']
filters = [[ 'project','is', {'type':'Project', 'id':74 } ]]
"""

cmd_shot = """
result =  sg.find( 'Shot', filters, fields )
print  '#results: ', len(result)
print "RESULT: ", result[0]
"""

cmd_version = """
result =  sg.find( 'Version', filters, fields )
print  '#results: ', len(result)
print "RESULT: ", result[0]
"""

t = timeit.Timer( cmd_shot, setup )
print t.repeat(3,1)


t = timeit.Timer( cmd_version, setup )
print t.repeat(3,1)
