import re
import redis
import pickle

#result =  sg.find( 'Version', filters, fields )
#print  '#results: ', len(result)
#print "RESULT: ", result[0]
results = []

rd = redis.Redis('localhost')
if rd.exists( -3689653915491585144 ):
	results =  pickle.loads( rd.get( -3689653915491585144 ) ) 


shots = []
for result in results:
	shots.append( result['code'] )
	
print shots
print ">>"
print [ shot for shot in shots if re.match( '.*gl.*', shot) ]
