from pymongo import Connection

if __name__ == '__main__':

    connection = Connection()
    db = connection.linux_laptops

    docs = db.docs
    re_os = '.*(?:linux|ubuntu|jolicloud).*'
    fields = ['Title', 'Description', 'OperatingSystem']

    def get_docs(field):
        ds = {}
        by_field = docs.find({field: {'$regex': re_os, '$options': 'i'}});
        print "Matches for field %s: %d" % (field, by_field.count())
        for d in by_field:
            if ds.has_key(d['_id']) is False:
                ds[d['_id']] = d
        return ds

    all_docs = {}
    for f in fields:
        all_docs.update(get_docs(f))

    print "Number of combined docs: %d" % len(all_docs)

