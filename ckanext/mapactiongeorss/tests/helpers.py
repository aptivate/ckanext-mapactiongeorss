import ckan.tests.helpers as helpers
import ckan.plugins as plugins


class FunctionalTestBaseClass(helpers.FunctionalTestBase):
    @classmethod
    def setup_class(cls):
        super(FunctionalTestBaseClass, cls).setup_class()
        plugins.load('mapactiongeorss')
