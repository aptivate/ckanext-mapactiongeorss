from webhelpers.feedgenerator import GeoAtom1Feed, rfc3339_date

from ckan.common import _
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class MapactiongeorssPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFeed)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactiongeorss')

    # IFeed
    def get_feed_class(self):
        return MapActionFeed

    def get_item_additional_fields(self, package):
        """ Get the geometry from either extras (for legacy datasets) or dataset
        fields """
        geometry_fields = ('ymin', 'xmin', 'ymax', 'xmax')
        geometry_source = {}

        if all(o in package for o in geometry_fields):
            geometry_source = package
        else:
            try:
                # look for geometry in extras
                geometry_source = {e['key']: e['value'] for e in package['extras']}
            except KeyError:
                pass

        box = tuple(
            float(geometry_source.get(n, '0'))
            for n in geometry_fields
        )
        return {'geometry': box}

    # IRoutes
    def before_map(self, map):
        map.connect(
            'mapaction_georss_dataset',
            '/feeds/dataset.atom',
            controller='feed',
            action='general')

        map.connect(
            'mapaction_georss_event',
            '/feeds/custom.atom',
            controller='feed',
            action='custom')

        return map


class MapActionFeed(GeoAtom1Feed):
    def __init__(self, title, link, description, **kwargs):
        super(MapActionFeed, self).__init__(
            _('MapAction GeoRSS Feed'),
            link,
            description,
            **kwargs
        )

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
