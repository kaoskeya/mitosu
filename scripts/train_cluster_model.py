import pickle
import pandas
import sklearn.cluster
from sklearn.externals import joblib

class ClusterModel():
    def __init__(self, model):
        self.model = model

        self.centroids = pandas.DataFrame(model.cluster_centers_,
                                          columns=['group_size',
                                                   'margin_total',
                                                   'n_items', 'total_bill'])

        self.centroids['cluster_name'] = self.centroids['margin_total'].rank()
        self.label_map = dict(zip(self.centroids.index.values,
                              self.centroids['cluster_name']))
        self.centroids_lkp = self.centroids.set_index(['cluster_name'])


    def dist_next_cluster(self, x):
        next_clust = int(x['cluster_name'] + 1)

        if next_clust > 3:
            return 0 
        
        y = self.centroids_lkp.ix[next_clust]
        return pandas.np.sqrt(
            pandas.np.power((x['group_size'] - y['group_size']), 2)
            + pandas.np.power((x['margin_total'] - y['margin_total']), 2)
            + pandas.np.power((x['n_items'] - y['n_items']), 2)
            + pandas.np.power((x['total_bill'] - y['total_bill']), 2)
        )


    def predict(self, x):
        label = model.predict(x)[0]
        return self.label_map[label]


with open("../data/gen.pkl") as f:
    d = pickle.load(f)
    
recs = []
for i in d:
    recs.append({
    "group_size" : i['group_size'],
    "margin_total" : sum([x['Margin'] * x['Price'] for x in i['detailed_items']]),
    "n_items" : len(i['items']),
    "total_bill" : sum([x['Price'] for x in i['detailed_items']])
})
    
df = pandas.DataFrame(recs)
model = sklearn.cluster.KMeans(n_clusters=3)
model.fit(df.as_matrix())
joblib.dump(model, "../data/models/kmeans")

# cm = ClusterModel(model)
