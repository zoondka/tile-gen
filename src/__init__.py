from os.path import dirname, join as pathjoin, realpath
from urlparse import urlparse
from ModestMaps.Core import Coordinate
import json
import Core
import Config

def parse_config_file(configpath):
    """ Parse a configuration file and return a Configuration object.

        Configuration file is formatted as JSON with two sections, "cache" and "layers":

          {
            "cache": { ... },
            "layers": {
              "layer-1": { ... },
              "layer-2": { ... },
              ...
            }
          }

        The full path to the file is significant, used to
        resolve any relative paths found in the configuration.

        See the Caches module for more information on the "caches" section,
        and the Core and Providers modules for more information on the
        "layers" section.
    """

    config_dict = json.load(open(configpath))

    scheme, host, path, p, q, f = urlparse(configpath)

    if scheme == '':
        scheme = 'file'
        path = realpath(path)

    dirpath = '%s://%s%s' % (scheme, host, dirname(path).rstrip('/') + '/')

    return Config.buildConfiguration(config_dict, dirpath)

def unknown_layer_message(config, unknown_layername):
    """ A message that notifies that the given layer is unknown and lists out the known layers. """

    return '"%s" is not a layer I know about. \n' + \
           'Here are some that I do know about: \n %s.' % \
           (unknown_layername, '\n '.join(sorted(config.layers.keys())))

def get_tile(layer, z, x, y, ext):
   """ Get a type string and tile binary for a given request layer tile. """

   config = parse_config_file("tilestache.cfg")

   # maybe do some other config checks as before
   if layer not in config.layers:
       raise Core.KnownUnknown(unknownLayerMessage(config, layer))

   tile = config.layers[layer].getTileResponse(Coordinate(x, y, z), ext, False, False)
   return tile
