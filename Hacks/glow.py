import math
from ctypes import *

from Process.Structures import *
from Utils import time
from offsets import *

from API.entity import *

def main(csgo):
	client = csgo.modules["client.dll"]
	while 1:
		time.sleep(1)
		player = Player()
		glow_object = csgo.read(client + dwGlowObjectManager, c_int)
		for entity in {Entity(i) for i in range(1, 16)}:
			if entity.is_valid and not entity.team == player.team:
				e_health = entity.health / 100
				index = csgo.read(entity.base + m_iGlowIndex, c_int)
				address = glow_object + index * 0x38
				g_object = csgo.read(address, GlowObject)
				g_object.r = 1.0 - e_health
				g_object.g = e_health
				g_object.b = 0.0
				g_object.a = 0.65
				g_object.renderWhenOccluded = False
				g_object.renderWhenUnoccluded = True
				g_object.fullBloom = False
				csgo.write(address, g_object, GlowObject)
