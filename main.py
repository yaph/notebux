import data
import codecs
import os
from jinja2 import Environment, PackageLoader

def create_pages():
    pass

def create_file(directory, name):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return codecs.open(os.path.join(directory, name), encoding='utf-8', mode='w')

if __name__ == '__main__':

    print "\n".join(['############################' for i in range(3)])

    path_root = os.getcwd()
    path_static = os.path.join(path_root, 'static')
    path_tpl = os.path.join(path_root, 'templates')
    path_dest = os.path.join(path_root, '_site')

    docs = data.get_docs()
    print "Number of docs: %d" % len(docs)

    indexes = data.get_indexes(docs)
    print "Number of indexes: %d" % len(indexes)

    # create pages from templates
    env = Environment(loader=PackageLoader('notebux', 'templates'))
    template_page = env.get_template('page.html')

    # create 1st 10 pages
    l = 1
    c = 0
    products = []
    for asin in docs:
        d = docs[asin]
        c += 1
        if c > l:
            break

        html = template_page.render(doc=d, base=path_dest, indexes=indexes)
        path_page = 'products/%s/' % d['ASIN']
        path_file = os.path.join(path_dest, path_page)

        f = create_file(path_file, 'index.html')
        f.write(html)
        f.close()

    # create index
    template_page = env.get_template('index.html')
    html = template_page.render(base=path_dest, index=indexes['index'])

    f = create_file(path_dest, 'index.html')
    f.write(html)
    f.close()

#    operatingsystems = indexes['OperatingSystem']
#    print "Number of operatingsystems: %d" % len(operatingsystems)

#    operatingsystems = sorted(operatingsystems.items(), key=lambda e: len(e[1]), reverse=True)
#    for os, docs in operatingsystems:
#        print os, len(docs)
#        print '\n'.join([d['URL'] for d in docs])

