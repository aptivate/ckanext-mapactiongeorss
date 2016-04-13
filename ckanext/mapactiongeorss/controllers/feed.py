from webhelpers.feedgenerator import GeoAtom1Feed
from ckan.controllers.feed import FeedController


class MapActionGeoRssFeedController(FeedController):
    def create_feed(self, title, link, description, **kwargs):
        return GeoAtom1Feed(title, link, description, **kwargs)

    def get_item_extras(self, package):
        extras = {e['key']: e['value'] for e in package['extras']}

        box = tuple(float(extras.get(n, '0'))
                    for n in ('ymin', 'xmin', 'ymax', 'xmax'))
        extras = {'geometry': box}

        return extras
