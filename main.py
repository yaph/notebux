import data
import shutil
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
    path_static = os.path.join(path_root, 'notebux/static')
    path_tpl = os.path.join(path_root, 'templates')
    path_dest = os.path.join(path_root, '_site')
    path_base = ''

    # copy static files
    shutil.rmtree(path_dest)
    shutil.copytree(path_static, path_dest)

    docs = data.get_docs()
    print "Number of docs: %d" % len(docs)

    indexes = data.get_indexes(docs)
    print "Number of indexes: %d" % len(indexes)

    # create pages from templates
    env = Environment(loader=PackageLoader('notebux', 'templates'))
    template_page = env.get_template('page.html')

    # cache templates after rendering
    template_cache = {}

    # create 1st 1000 pages
    l = 1000
    c = 0
    products = []
    for asin in docs:
        d = docs[asin]
        c += 1
        if c > l:
            break

        html = template_page.render(doc=d, base=path_base, indexes=indexes)
        path_page = 'products/%s/' % d['ASIN']
        path_file = os.path.join(path_dest, path_page)

        f = create_file(path_file, 'index.html')
        f.write(html)
        f.close()

    # create main index
    template_page = env.get_template('index.html')
    html = template_page.render(base=path_base, index=indexes['index'])
    f = create_file(path_dest, 'index.html')
    f.write(html)
    f.close()

    del indexes['index']
    for i in indexes:
        for name in indexes[i]:
            html = template_page.render(base=path_base, index=indexes[i][name])
            path_index = "%s/%s/%s" % (path_dest, i.lower(), name.lower())
            f = create_file(path_index, 'index.html')
            f.write(html)
            f.close()

#    operatingsystems = indexes['OperatingSystem']
#    print "Number of operatingsystems: %d" % len(operatingsystems)

#    operatingsystems = sorted(operatingsystems.items(), key=lambda e: len(e[1]), reverse=True)
#    for os, docs in operatingsystems:
#        print os, len(docs)
#        print '\n'.join([d['URL'] for d in docs])

