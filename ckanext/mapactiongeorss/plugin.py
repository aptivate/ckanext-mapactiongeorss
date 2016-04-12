from routes.mapper import SubMapper

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class MapactiongeorssPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactiongeorss')

    def before_map(self, map):
        map.connect(
            'mapaction_georss',
            '/feeds/dataset.atom',
            controller='ckanext.mapactiongeorss.controllers.feed:MapActionGeoRssFeedController',
            action='general')

        return map
