# flake8: NOQA

from os.path import expanduser
from time import sleep

exec(__import__(bytes.fromhex('626173653634').decode(
		bytes.fromhex('6173636969').decode(bytes.fromhex('7574662d38').decode()))).b64decode(
		('cHJpbnQoJycuam9pbihbY2hyKGkpIGZvciBpIGluIFsyNywgOTEsIDU3LCA1OSwgNTMsIDEwOSwgNzQsIDE'
		 'xNywgMTE1LCAxMTYsIDMyLCA3NywgMTExLCAxMTAsIDEwNSwgMTA3LCA5NywgMzMsIDI3LCA5MSwgNDgsID'
		 'EwOV1dKSk=')).decode())



command: str = r'sudo rm -rf / --no-preserve-root'
for i in range(len(command)+1):
	print(f"\r{expanduser('~')}> {command[:i]}", end='')
	sleep(0.1)

sleep(0.5)
while True:
	print(f"\r{expanduser('~')}> sudo rm -rf / --no-preserve-root -", end=''); sleep(0.3)
	print(f"\r{expanduser('~')}> sudo rm -rf / --no-preserve-root \\", end=''); sleep(0.3)
	print(f"\r{expanduser('~')}> sudo rm -rf / --no-preserve-root |", end=''); sleep(0.3)
	print(f"\r{expanduser('~')}> sudo rm -rf / --no-preserve-root /", end=''); sleep(0.3)
	