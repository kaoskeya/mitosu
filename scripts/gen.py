import pandas
from scipy import stats
import pprint

class CustDist():
    def __init__(self, name, dist_csv=None, df=None):

        if dist_csv:
            self._df = pandas.read_csv(dist_csv)

        if df is not None:
            self._df = df

        self._dist = stats.rv_discrete(name = name,
                                       values = (self._df.index, 
                                                 self._df['Probability']))
        self._val_map = dict(zip(self._df.index, self._df['Value']))


    def rvs(self, size=None):
        series = self._dist.rvs(size=size)
        if not size or size == 1:
            series = [series]

        recs = []
        for rec in series:
            res = self._val_map[rec]
            recs.append(res)

        # return map(lambda x: self._val_map[x], series)
        return recs


    def rv(self):
        result =  self.rvs()[0]
        return result

class PersonaCategoriesDist():
    def __init__(self, name, dist_csv):
        self._dists = {}
        self._df = pandas.read_csv(dist_csv)

        for col in filter(lambda x: x !='Value', self._df.columns):
            _df = self._df[['Value', col]]
            _df = _df.rename(columns={col : 'Probability'})
            self._dists[col] = CustDist(col, df=_df)

    def rvs(self, persona, size=None):
        return self._dists[persona].rvs(size=size)

    def rv(self, persona):
        return self.rvs(persona)[0]


class SpenderItemDist():
    def __init__(self, name, dist_csv):
        self._df = pandas.read_csv(dist_csv)
        cats = self._df['Category Name'].unique()

        self._dists = {}

        for col in filter(lambda x: x not in ['Value', 'Category Name'],
                           self._df.columns):
            self._dists[col] = {}
            _df = self._df[['Category Name', 'Value', col]]
            _df = _df.rename(columns={col : 'Probability'})

            _df = _df.dropna()

            for cat in cats:
                cat_df = _df[_df['Category Name'] == cat]
                self._dists[col][cat] = CustDist('_'.join([col, cat]),
                                                 df=cat_df)

    def rvs(self, spender, category, size=None):
        return self._dists[spender][category].rvs(size=size)

    def rv(self, spender, category):
        return self.rvs(spender, category)[0]


# Metadata
categories_df = pandas.read_csv("../data/metadata/categories.csv")
items_df = pandas.read_csv("../data/metadata/items.csv")
items_df = items_df.set_index(['Name'])

# print items_df

# Group and Persona and Spender Dists
group_dist = CustDist("group_size", "../data/metadata/group_size_dist.csv")
persona_dist = CustDist("persona", "../data/metadata/persona_dist.csv")
spender_dist = CustDist("spender", "../data/metadata/spender_dist.csv")

# Persona -> Category Dist
categories_dist = PersonaCategoriesDist("categories",
                               "../data/metadata/persona_categories_dist.csv")

# Spender -> Item Dist
items_dist = SpenderItemDist("items",
                                     "../data/metadata/spender_item_dist.csv")

recs = []

with open("../data/gen.dat", 'w') as f:
    for i in xrange(10000):

        group_size = group_dist.rv()
        group = [(i, persona_dist.rv(), spender_dist.rv())
                 for i in xrange(group_size)]
        bill_cats = set([])
        items = {}
        person_categories = {}
        detailed_items = []


        for i, persona, spender in group:
            categories = categories_dist.rv(persona).split(", ")

            person_categories[(i, persona, spender)] = categories

            bill_cats.update(categories)
            for category in categories:


                item = items_dist.rv(spender, category)

                if item == "NULL":
                    continue
                items[((i, persona, spender), category)] = item

                detailed_item = items_df.ix[item]
                detailed_items.append(detailed_item)


        bill = {
            "group_size" : group_size,
            "group" : group,
            "categories" : bill_cats,
            "_items" : items,
            "items" : items.values(),

            "detailed_items" : detailed_items,

            "person_categories" : person_categories
        }
        try:
            print >>f, ' '.join(map(lambda x: x['Id'], detailed_items))
        except TypeError, e:
            print e
        else:
            recs.append(bill)


import pickle
with open("../data/gen.pkl", 'w') as f:
    pickle.dump(recs, f)