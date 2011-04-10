from shotgun.api.shotgun_api3 import Shotgun
from shotgun.api.redis_api3 import Redis

rd = Redis()
sg = Shotgun( 'https://baseblack.shotgunstudio.com', 'NewVersion', 'df403e9631a26b4c018be400ba048e8bc404b845')

