import requests
from bs4 import BeautifulSoup

def _get_open_graph_data(url):
    """get graph basic"""
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        og_data = {}

        og_image_tag = soup.find('meta', property='og:image')
        og_data['image'] = og_image_tag.get('content') if og_image_tag else None
        
        og_title_tag = soup.find('meta', property='og:title')
        og_data['title'] = og_title_tag.get('content') if og_title_tag else None

        og_description_tag = soup.find('meta', property='og:description')
        og_data['description'] = og_description_tag.get('content') if og_description_tag else None
        
        return og_data, soup
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None


class ResourceParseBase:
    """every url is a resource and we can parse the metadata for it"""
    def handle(self, soup):
        """
        base implements
        """
        return {}
            
    def parse_many(self, key, mapping):
            m = mapping[key]
            r= self.soup.find_all('meta',  m)
            r =  [c['content'] for c in r]
            return r
        
    def parse_one(self,  key, mapping):
        r = self.parse_many(self.soup,key, mapping)
        if r: 
            return r[0]
            
    def _run(self,url):
        data, self.soup = _get_open_graph_data(url)
        data.update(self.handle(self.soup, data))
        return data
    
    def __call__(self, url):
        return self._run(url)

 
class Arxiv(ResourceParseBase):
    def handle(self, soup, data=None):
        return {
            'image' : f"https://arxiv.org{data.get('image')}",
            'authors':"; ".join(list(map(lambda x: x['content'], 
                                            soup.find_all('meta', {'name':'citation_author'}))))}

class Amazon(ResourceParseBase):
    def handle(self, soup, data):
        return super().handle(soup)
 

class GoodReads(ResourceParseBase):
    def handle(self, soup, data):
        return super().handle(soup)
 
class GoogleScholarBib(ResourceParseBase):
    def handle(self, soup, data):
        return super().handle(soup)
 
#test nature and other journals 
 
PROVIDERS = {
    "arxiv.org"  : Arxiv(),
    "amazon.com" : Amazon(),
    "goodreads.com" : GoodReads(),
    "scholar.googleusercontent.com": GoogleScholarBib()
}


def update_config():
    """add database stuff to the providers"""
    pass
