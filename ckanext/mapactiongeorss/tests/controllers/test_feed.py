from defusedxml.ElementTree import fromstring
from webhelpers.feedgenerator import rfc3339_date
import nose.tools

import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
import ckan.tests.factories as factories

import ckanext.mapactiongeorss.tests.helpers as helpers

assert_equals = nose.tools.assert_equals
assert_true = nose.tools.assert_true
assert_regexp_matches = nose.tools.assert_regexp_matches


class TestMapActionGeoRssFeedController(helpers.FunctionalTestBaseClass):
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

    def test_feed_contains_updated(self):
        dataset = factories.Dataset()

        updated = self._find_in_rss('xmlns:entry/xmlns:updated').text

        expected_updated = self._convert_date(dataset['metadata_modified'])
        assert_equals(updated, expected_updated)

    def _convert_date(self, date):
        return rfc3339_date(h.date_str_to_datetime(date)).decode('utf-8')

    def _find_in_rss(self, path):
        url = toolkit.url_for('mapaction_georss')
        response = self.app.get(url, status=[200])

        et = fromstring(response.body)
        namespaces = {'xmlns': 'http://www.w3.org/2005/Atom',
                      'georss': 'http://www.georss.org/georss'}

        elements = et.find(path, namespaces=namespaces)

        assert_true(elements is not None,
                    "Couldn't find elements matching path {0} in feed".format(
                        path))

        return elements
