This wrapper is a very light wrapper around the MonoGame 'Game' class.
It provides an initialize, update, and draw event, that the main source py file (/src/__init__.py) subscribes to. (As pythonnet does not allow overriding of these methods.)
This does not do anything beyond that, everything else is done entirely in python.