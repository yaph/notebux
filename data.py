from pymongo import Connection

def _get_docs(docs, field):
    re_os = '.*(?:linux|ubuntu|jolicloud).*'
    ds = {}
    by_field = docs.find({field: {'$regex': re_os, '$options': 'i'}});
    for d in by_field:
        if ds.has_key(d['ASIN']) is False:
            ds[d['ASIN']] = d
    return ds

def get_docs():
    """Get all Linux related docs as a dictionary keyed by ASIN."""
    fields = ['Title', 'Description', 'OperatingSystem']
    all_docs = {}

    connection = Connection()
    db = connection.linux_laptops
    docs = db.docs

    for f in fields:
        all_docs.update(_get_docs(docs, f))
    return all_docs

def get_indexes(docs):
    """Get indexes of docs grouped by attribute."""
    indexes = {'index':[]}
    attr = ['Brand', 'OperatingSystem', 'Manufacturer']

    for asin in docs:
        doc = docs[asin]
        indexes['index'].append(doc)
        for a in attr:
            if doc.has_key(a):
                val = doc[a]
                if indexes.has_key(a) is False:
                    indexes[a] = {}
                if indexes[a].has_key(val) is False:
                    indexes[a][val] = []
                indexes[a][val].append(doc)
    return indexes
