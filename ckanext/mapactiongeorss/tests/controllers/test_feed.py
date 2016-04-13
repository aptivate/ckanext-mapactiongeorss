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

        title = self._find_in_rss('xmlns:entry/xmlns:title').text

        assert_equals(title, dataset['title'])

    def test_feed_contains_coordinates(self):
        metadata = {
            'ymin': '-2373790',
            'xmin': '2937940',
            'ymax': '-1681290',
            'xmax': '3567770',
        }

        extras = [
            {'key': k, 'value': v} for (k, v) in
            metadata.items()
        ]

        factories.Dataset(extras=extras)

        box = self._find_in_rss('xmlns:entry/georss:box').text

        expected_values = {k: float(metadata[k])
                           for (k, v) in metadata.items()}

        expected_box = '{ymin:f} {xmin:f} {ymax:f} {xmax:f}'.format(
            **expected_values)

        assert_equals(box, expected_box)

    def _find_in_rss(self, path):
        url = toolkit.url_for('mapaction_georss')
        response = self.app.get(url, status=[200])

        et = fromstring(response.body)
        namespaces = {'xmlns': 'http://www.w3.org/2005/Atom',
                      'georss': 'http://www.georss.org/georss'}

        return et.find(path, namespaces=namespaces)
