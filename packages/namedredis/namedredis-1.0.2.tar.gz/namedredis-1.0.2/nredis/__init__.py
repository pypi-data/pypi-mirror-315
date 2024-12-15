# coding=utf8
""" Named Redis

Handles connections to specific servers using names and config
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-09-23"

# Limit exports
__all__ = [ 'nr', 'reset' ]

# Ouroboros imports
from config import config
from tools import compare
import undefined

# Pip imports
from redis import StrictRedis

__cons = {}
"""Connections

The list of current connections and configs by name"""

def nr(name: str) -> StrictRedis:
	"""Named Redis

	Returns an existing connection, or else fetches the details using config \
	to create a new connection and return that. If the connection is not found \
	in config, then default localhost:6379:0 using RESP3 will be used

	Arguments:
		name (str): The name of the connection to be found in config

	Returns:
		StrictRedis
	"""

	global __cons

	# Try to return the existing connection
	try:
		return __cons[name]['r']

	# If we don't have the connection, pass to the next phase
	except KeyError:
		pass

	# Get the connection out of config
	dConf = config.redis[name]({
		'host': 'localhost',
		'port': 6379,
		'db': 0,
		'protocol': 3
	})

	# Go through each existing config
	for k in __cons:

		# If the config is the same
		if compare(__cons[k]['d'], dConf):

			# Store it under the new name as well
			__cons[name] = __cons[k]

			# Then return the connection
			return __cons[name]['r']

	# Create and store a new connection using the config
	__cons[name] = {
		'd': dConf,
		'r': StrictRedis(**dConf)
	}

	# Return the new connection
	return __cons[name]['r']

def reset(name: str = undefined) -> bool:
	"""Reset

	Clears all existing connections.

	Arguments:
		name (str): Optional argument, name of the connection to reset. If not \
			set, resets all currently open connections.

	Returns:
		bool
	"""

	global __cons

	# If we have no name
	if name is undefined:

		# Step through each existing connection
		for s in __cons:

			# Deleting the instance, closing the connection
			del __cons[s]

		# Return OK
		return True

	# Else, we have a specific name, try to delete it and close the connection
	try:
		del __cons[name]
		return True
	except KeyError:
		return False