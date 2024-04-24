import ckan.tests.factories as factories


class Dataset(factories.Dataset):
    type = 'test_schema'

class DefaultDataset(factories.Dataset):
    type = 'default'
