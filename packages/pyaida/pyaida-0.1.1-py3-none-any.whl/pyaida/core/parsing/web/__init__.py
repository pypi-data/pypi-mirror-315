
from . providers import PROVIDERS, _get_open_graph_data

def get_provider(url:str):
    """determine if we have a custom provider for the url"""
    return PROVIDERS.get(url)


def get_open_graph_data(url:str):
    """look for a url specific provider or use the default"""
    provider = get_provider(url)
    if provider:
        return provider(url)
    return _get_open_graph_data(url)[0]
