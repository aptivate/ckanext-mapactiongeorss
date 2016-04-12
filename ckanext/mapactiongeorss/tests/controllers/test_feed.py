from defusedxml.ElementTree import fromstring
import nose.tools

import ckan.plugins.toolkit as toolkit
import ckan.tests.factories as factories

import ckanext.mapactiongeorss.tests.helpers as helpers

assert_equals = nose.tools.assert_equals
assert_true = nose.tools.assert_true
assert_regexp_matches = nose.tools.assert_regexp_matches


class TestMapActionGeoRssFeedController(helpers.FunctionalTestBaseClass):
    def test_feed_contains_dataset(self):
        dataset = factories.Dataset()

        url = toolkit.url_for(controller='feed', action='general')
        response = self.app.get(url, status=[200])

        import ipdb
        ipdb.set_trace()

        et = fromstring(response.body)
        namespace = '{http://www.w3.org/2005/Atom}'
        path = '{namespace}entry/{namespace}title'.format(namespace=namespace)
        title = et.find(path).text

        assert_equals(title, dataset['title'])
