from webhelpers.feedgenerator import GeoAtom1Feed
from ckan.controllers.feed import FeedController


class MapActionGeoRssFeedController(FeedController):
    def create_feed(self, title, link, description, **kwargs):
        return GeoAtom1Feed(title, link, description, **kwargs)

    def get_item_extras(self, package):
        names = ('ymin', 'xmin', 'ymax', 'xmax')

        extras = {e['key']: e['value'] for e in package['extras']}
        coords = {n: float(extras.get(n, 0)) for n in names}

        box = tuple(v for (_, v) in coords.items())

        y = (coords['ymin'] + coords['ymax']) / 2
        x = (coords['xmin'] + coords['xmax']) / 2

        point = (y, x)

        return {'geometry': box,
                'geometry': point}
