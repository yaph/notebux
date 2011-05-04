from pymongo import Connection
from amazonproduct.api import API
from config import AWS_KEY, SECRET_KEY

if __name__ == '__main__':

    item_attr = ['Brand', 'Manufacturer', 'Model', 'OperatingSystem', 'Title']
    item_img = ['SmallImage', 'MediumImage', 'LargeImage']
    item_offer = ['SalesRank', 'LowestNewPrice', 'TotalNew']
    img_attr = ['Height', 'URL', 'Width']

    connection = Connection()
    db = connection.linux_laptops

    api = API(AWS_KEY, SECRET_KEY, 'us')
    paginator = api.item_search('Electronics', Keywords='linux laptop', ResponseGroup='Medium')

    for root in paginator:
        nspace = root.nsmap.get(None, '')
        items = root.xpath('//aws:Items/aws:Item', namespaces={'aws' : nspace})

        for i in items:
            doc = {}
            try:
                doc['_id'] = str(i.ASIN)
                doc['URL'] = str(i.DetailPageURL)

                # Images
                doc['Images'] = {}
                for a in item_img:
                    if hasattr(i, a):
                        img = i[a]
                        doc['Images'][a] = {}
                        for ia in img_attr:
                            if hasattr(img, ia):
                                doc['Images'][a][ia] = str(img[ia])

                # ItemAttributes
                for a in item_attr:
                    if hasattr(i.ItemAttributes, a):
                        doc[a] = unicode(i.ItemAttributes[a])

                # OfferSummary
                for a in item_offer:
                    if hasattr(i.OfferSummary, a):
                        doc[a] = unicode(i.OfferSummary[a])

                if hasattr(i.EditorialReviews.EditorialReview, 'Content'):
                    doc['Description'] = unicode(i.EditorialReviews.EditorialReview.Content)

                print "Inserting document"
                print doc
                db.docs.insert(doc)

            except AttributeError, e:
                print e
#            else:
#                print dir(i)
