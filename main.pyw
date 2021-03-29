from threading import Thread
from keyboard import is_pressed

import Hacks
from Process import Process
from Utils import time

import logging
from rich import pretty, traceback
from rich.logging import RichHandler
from rich.console import Console

pretty.install()
traceback.install()


format_ = '%(message)s.'
logging.basicConfig(format=format_, level='DEBUG', handlers=[RichHandler()])

log = logging.getLogger()

console = Console()

from API.entity.entity import Entity

def wrapper(func, handler):
	try:
		func(handler)
	except Exception as e:
		log.error(e)
		console.print_exception()

def main():

	console.clear()

	handler = Process('csgo.exe')

	# Injection
	Entity.handler = handler

	cheat_set = {
		lambda: wrapper(Hacks.glow.main, handler),
		lambda: wrapper(Hacks.bhop.main, handler),
		lambda: wrapper(Hacks.trigger.main, handler),
		lambda: wrapper(Hacks.radarhack.main, handler),
		lambda: wrapper(Hacks.aimbot.main, handler)
	}

	for t in cheat_set:
		Thread(target=t, daemon=True).start()

	while(not is_pressed("insert")):
		time.sleep(10)

	exit()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		exit()
