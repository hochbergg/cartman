import random

DEFAULT_LENGTH = 16

def generateRandomId(length):
  """
  Generates a random ID string of the given length.
  """
  return "".join(str(random.randint(0, 9)) for d in range(length))

def randomIdGenerator(prefix="", length=None):
  """
  Returns a random ID generator function.
  """
  if not length:
    length = DEFAULT_LENGTH
  length -= len(prefix)
  return lambda: prefix + generateRandomId(length)
