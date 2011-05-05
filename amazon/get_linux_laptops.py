from pymongo import Connection
from amazonproduct.api import API
from config import AWS_KEY, SECRET_KEY

if __name__ == '__main__':

    item_attr = ['Brand', 'Manufacturer', 'Model', 'OperatingSystem', 'ProductGroup', 'ProductTypeName', 'ReleaseDate', 'Title']
    item_img = ['SmallImage', 'MediumImage', 'LargeImage']
    item_offer = ['SalesRank', 'TotalNew']
    item_price = ['LowestNewPrice', 'LowestRefurbishedPrice', 'LowestUsedPrice']
    img_attr = ['Height', 'URL', 'Width']

    connection = Connection()
    db = connection.linux_laptops

    api = API(AWS_KEY, SECRET_KEY, 'us', associate_tag='notebux-20')
    paginator = api.item_search('Electronics', Keywords='linux laptop', ResponseGroup='Medium')

    for root in paginator:
        nspace = root.nsmap.get(None, '')
        items = root.xpath('//aws:Items/aws:Item', namespaces={'aws' : nspace})

        for i in items:
            doc = {}
            try:
                doc['ASIN'] = str(i.ASIN)
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
                        doc[a] = int(i.OfferSummary[a])

                # Prices
                for a in item_price:
                    if hasattr(i.OfferSummary, a) and hasattr(i.OfferSummary[a], 'Amount'):
                        doc[a] = i.OfferSummary[a].Amount / 100.0

                # ListPrice 'ListPrice'
                if hasattr(i.ItemAttributes, 'ListPrice') and hasattr(i.ItemAttributes.ListPrice, 'Amount'):
                    doc['ListPrice'] = i.ItemAttributes.ListPrice.Amount / 100.0

                if hasattr(i, 'EditorialReviews') and hasattr(i.EditorialReviews.EditorialReview, 'Content'):
                    doc['Description'] = unicode(i.EditorialReviews.EditorialReview.Content)

                print "Upserting document"
                print doc
                spec = {'ASIN': doc['ASIN']}
                db.docs.update(spec, doc, True)

            except AttributeError, e:
                print e
#            else:
#                print dir(i)
