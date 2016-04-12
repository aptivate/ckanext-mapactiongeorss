from defusedxml.ElementTree import fromstring
import nose.tools

import ckan.plugins.toolkit as toolkit
import ckan.tests.factories as factories

import ckanext.mapactiongeorss.tests.helpers as helpers

assert_equals = nose.tools.assert_equals
assert_true = nose.tools.assert_true
assert_regexp_matches = nose.tools.assert_regexp_matches


class TestMapActionGeoRssFeedController(helpers.FunctionalTestBaseClass):
    controller = 'ckanext.mapactiongeorss.controllers.feed:MapActionGeoRssFeedController'

    def test_feed_contains_dataset(self):
        dataset = factories.Dataset()

        url = toolkit.url_for('mapaction_georss')
        response = self.app.get(url, status=[200])

        et = fromstring(response.body)
        namespace = '{http://www.w3.org/2005/Atom}'
        path = '{namespace}entry/{namespace}title'.format(namespace=namespace)
        title = et.find(path).text

        assert_equals(title, dataset['title'])

    def test_feed_contains_coordinates(self):
        metadata = {
            'xmin': '-506691.09',
            'xmax': '1493308.91',
            'ymin': '208909.14',
            'ymax': '1268909.14',
        }

        extras = [
            {'key': k, 'value': v} for (k, v) in
            metadata.items()
        ]

        factories.Dataset(extras=extras)

        url = toolkit.url_for('mapaction_georss')
        response = self.app.get(url, status=[200])

        et = fromstring(response.body)
        namespace = '{http://www.w3.org/2005/Atom}'
        path = '{namespace}entry/{namespace}georss:box'.format(
            namespace=namespace)
        box = et.find(path).text

        expected_box = '{xmin} {ymin} {xmax} {ymax}'.format(
            **metadata)
        assert_equals(box, expected_box)
