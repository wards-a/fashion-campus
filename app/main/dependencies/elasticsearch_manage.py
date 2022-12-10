from elasticsearch import Elasticsearch, helpers

ES_URL = "http://elastic:openes101@34.87.68.255:9200"

class ES:
    resp = None

    def __init__(self) -> None:
        self.es_client = Elasticsearch(ES_URL)

    def create_index(self, index: str, mappings: dict, settings: dict = None):
        self.es_client.indices.create(index=index, mappings=mappings, settings=settings)

    def delete_index(self, index: str):
        self.es_client.indices.delete(index=index)
    
    def get_index_mapping(self, index: str):
        # set resp
        self.resp = self.es_client.indices.get_mapping(index=index)
        return self.resp
    
    def get_all_data(self, index: str):
        # set resp
        return helpers.scan(self.es_client, query={"query":{ "match_all": {}}}, index=index)

    def get_pagination_data(self, **kwargs):
        # set resp
        self.resp = self.es_client.search(**kwargs)
        return self.resp

    def get_specific_data(self, index: str, query: dict):
        # set resp
        self.resp =  self.es_client.search(index=index, query=query)
        return self.resp
    
    # get doc id from resp
    def get_doc_id(self):
        doc_id = list()
        try:
            for i in range(len(self.resp['hits']['hits'])):
                _id = self.resp['hits']['hits'][i]['_id']
                doc_id.append(_id)
        except TypeError:
            return {"message": "Response not available, get data first"}, 404
        except IndexError:
            return {"message": "No item available"}, 404
        return doc_id
    
    def get_doc_value(self):
        doc_value = list()
        try:
            for hit in self.resp['hits']['hits']:
                doc_value.append(hit["_source"])
        except TypeError:
            return {"message": "Response not available, get data first"}, 404
        return doc_value

    def insert_item(self, index: str, data: dict):
        self.es_client.index(index=index, document=data)
    
    def update_item(self, index: str, id: str, data: str):
        self.es_client.update(index=index, id=id, doc=data)

    def update_item_by_query(self, index: str, query: dict, script: dict):
        self.es_client.update_by_query(index=index, query=query, script=script)

    def delete_item(self, index: str, id: str):
        self.es_client.delete(index=index, id=id)
    

### mappings object ###
products = {
    "properties": {
        "id": {"type": "keyword"},
        "category_id": {"type": "keyword"},
        "category_deleted": {"type": "boolean"},
        "name": {"type": "text", "analyzer": "search_name_analyzer"},
        "description": {"type": "text"},
        "size": {"type": "keyword"},
        "price": {"type": "integer"},
        "condition": {"type": "text"},
        "deleted": {"type": "boolean"},
        "images": {"type": "keyword"}
    }
}

analyzer = {
    "analysis": {
        "analyzer": {
            "search_name_analyzer": {
                "type": "custom",
                "tokenizer": "keyword",
                "filter": ["lowercase"]
            }
        }
    }
}

query = {
        "bool": {
            "must": [
                {
                    "wildcard": {"name": "*test*"}
                },
                {
                    "term": {"category_deleted": "false"}
                },
                # {
                #     "term": {"deleted": "false"}
                # },
                # {
                #     "range": {
                #         "price": {
                #             "gte": 1000,
                #             "lte": 100000
                #         }
                #     }
                # }
                # {
                #     "term": {"category_id": "a3359bfa-0c01-4464-9931-4bf13aed4456"}
                # },
                # {
                #     "term": {"category_id": "3e55b2eb-361c-46a5-b130-d1e462684392"}
                # }
            ]
            # "filter": [
            #     {
            #         "terms": {
            #             "category_id": ["2a42a4b3-a01d-44d8-a2ff-fffc5f022b94"]
            #         }
            #     }
            # ]
        }
    }

sort = [{"price":"asc"}]

script = {
    "source": "ctx._source.category_deleted='false'",
    "lang": "painless"
}

query2 = {
    "term": {
        "category_id": "45751527-cc14-4b94-95f4-bb7b930de1ee"
    }
}

es = ES()
# es.delete_index(index="products")
# es.create_index(index="products", mappings=products, settings=analyzer)
# es.insert_item(index="products_index", data=data)
# print(es.get_index_mapping(index="products"))
# resp = es.get_specific_data(index="products_index", query=query)
# print(es.get_pagination_data(index="products", query=query, from_=0, size=50, sort=sort))
# resp = es.get_all_data(index="products")
# print("Got %d Hits:" % es.resp['hits']['total']['value'])
# for hit in es.resp['hits']['hits']:
#     print("%(id)s %(name)s: %(price)s" % hit["_source"])
# for i in range(len(es.resp)):
#     doc_id = es.resp['hits']['hits'][i]['_id']
#     es.delete_item(index="products", id=doc_id)
# for e in resp:
#     print(e)
# print(list(resp))
# helpers.reindex(es.es_client, source_index="products_index", target_index="products")
# es.update_item_by_query(index="products", query=query2, script=script)
# print(es.get_doc_id())
# print(es.get_doc_value())