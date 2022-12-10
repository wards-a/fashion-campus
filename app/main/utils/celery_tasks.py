from google.cloud import storage

from app.main import celery, db
from app.main.utils.image_helper import gcs_bucket
from app.main.model.category import Category
from app.main.dependencies.elasticsearch_manage import ES


@celery.task(name="app.main.utils.celery_tasks.upload_to_gcs")
def upload_to_gcs(file):
    bucket = gcs_bucket()

    ## For slow upload speed
    storage.blob._DEFAULT_CHUNKSIZE = 2097152 # 1024 * 1024 B * 2 = 2 MB
    storage.blob._MAX_MULTIPART_SIZE = 2097152 # 2 MB

    blob = bucket.blob(file['filename'])
    blob.content_type = file['media_type']
    blob.upload_from_file(file['file'])

@celery.task(name="app.main.utils.celery_tasks.remove_from_gcs")
def remove_from_gcs(filename):
    bucket = gcs_bucket()

    blob = bucket.blob(filename)
    blob.delete()

@celery.task(name="app.main.utils.celery_tasks.insert_to_es")
def insert_to_es(product=None, images=None, category=None):
    es = ES()
    data = dict()
    boolean = {"0": "false", "1": "true"}
    _product = {
        "id": str(product.id),
        "category_id": str(product.category_id),
        "category_deleted": boolean[category.deleted.value],
        "name": product.name,
        "description": product.description,
        "size": ["S", "M", "L", "XL"],
        "price": int(product.price),
        "condition": product.condition.value,
        "deleted": "false",
    }
    data.update(_product)

    if images:
        data.update({"images": images})

    es.insert_item(index="products", data=data)

@celery.task(name="app.main.utils.celery_tasks.update_to_es")
def update_to_es(product=None, images=None, category=None):
    es = ES()
    data = dict()
    boolean = {"0": "false", "1": "true"}

    _product = {
        "id": str(product['id']),
        "category_id": str(product['category_id']),
        "category_deleted": boolean[category.deleted.value],
        "name": product['name'],
        "description": product['description'],
        "price": int(product['price']),
        "condition": product['condition']
    }
    data.update(_product)

    if images:
        data.update({"images": images})

    query = {
        "bool": {
            "must": {
                "term": {"id": product['id']}
            }
        }
    }

    es.get_specific_data(index="products", query=query)

    doc_id = es.get_doc_id()

    es.update_item(index="products", id=doc_id[0], data=data)

@celery.task(name="app.main.utils.celery_tasks.deleted_to_es")
def deleted_to_es(data: dict = None, field: str = None):
    es = ES()
    script = {
        "source": f"ctx._source.{field}='true'",
        "lang": "painless"
    }

    query = {
        "term": {
            data['key']: data['value']
        }
    }

    es.update_item_by_query(index="products", query=query, script=script)