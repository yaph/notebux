from pymongo import Connection
from operator import itemgetter

if __name__ == '__main__':

    print "\n".join(['############################' for i in range(6)])

    connection = Connection()
    db = connection.linux_laptops

    docs = db.docs
    re_os = '.*(?:linux|ubuntu|jolicloud).*'
    fields = ['Title', 'Description', 'OperatingSystem']
#    fields = ['OperatingSystem']

    def get_docs(field):
        ds = {}
        by_field = docs.find({field: {'$regex': re_os, '$options': 'i'}});
        print "Matches for field %s: %d" % (field, by_field.count())
        for d in by_field:
            if ds.has_key(d['ASIN']) is False:
                ds[d['ASIN']] = d

        return ds

    all_docs = {}
    for f in fields:
        all_docs.update(get_docs(f))

    print "Number of combined docs: %d" % len(all_docs)

    # add docs to indexes by attribute
    indexes = {}
    attr = ['Brand', 'OperatingSystem', 'Manufacturer']

    for asin in all_docs:
        doc = all_docs[asin]
        for a in attr:
            if doc.has_key(a):
                val = doc[a]
                if indexes.has_key(a) is False:
                    indexes[a] = {}
                if indexes[a].has_key(val) is False:
                    indexes[a][val] = []
                indexes[a][val].append(doc)

    operatingsystems = indexes['OperatingSystem']
    print "Number of operatingsystems: %d" % len(operatingsystems)

    operatingsystems = sorted(operatingsystems.items(), key=lambda e: len(e[1]), reverse=True)

    for os, docs in operatingsystems:
        print os, len(docs)
#        print docs
        print '\n'.join([d['URL'] for d in docs])

