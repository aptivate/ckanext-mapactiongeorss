from webhelpers.feedgenerator import GeoAtom1Feed, rfc3339_date
from ckan.controllers.feed import FeedController


class MapActionGeoRssFeedController(FeedController):
    def create_feed(self, title, link, description, **kwargs):
        return MapActionFeed(title, link, description, **kwargs)

    def get_item_extras(self, package):
        extras = {e['key']: e['value'] for e in package['extras']}

        box = tuple(float(extras.get(n, '0'))
                    for n in ('ymin', 'xmin', 'ymax', 'xmax'))
        extras = {'geometry': box}

        return extras


class MapActionFeed(GeoAtom1Feed):
    def add_item_elements(self, handler, item):
        """
        Add the <updated> and <published> fields to each entry that's written
        to the handler.
        """
        super(MapActionFeed, self).add_item_elements(handler, item)

        if (item['updated']):
            handler.addQuickElement(
                u'updated',
                self._convert_date(item['updated']).decode('utf-8'))

        if(item['published']):
            handler.addQuickElement(
                u'published',
                self._convert_date(item['published']).decode('utf-8'))

    def _convert_date(self, date):
        return rfc3339_date(date).decode('utf-8')
