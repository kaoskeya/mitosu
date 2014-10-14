import pandas
from sklearn.externals import joblib

class ClusterModel():
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

        self.centroids = pandas.DataFrame(self.model.cluster_centers_,
                                          columns=['group_size',
                                                   'margin_total',
                                                   'n_items', 'total_bill'])

        self.centroids['cluster_name'] = self.centroids['margin_total'].rank()
        self.label_map = dict(zip(self.centroids.index.values,
                              self.centroids['cluster_name']))
        self.centroids_lkp = self.centroids.set_index(['cluster_name'])
        print self.centroids_lkp.index

    def _get_dist(self, x, y):
        return pandas.np.sqrt(
            pandas.np.power((x['group_size'] - y['group_size']), 2)
            + pandas.np.power((x['margin_total'] - y['margin_total']), 2)
            + pandas.np.power((x['n_items'] - y['n_items']), 2)
            + pandas.np.power((x['total_bill'] - y['total_bill']), 2)
        )


    def dist_next_cluster(self, x):
        next_clust = int(x['cluster_name'] + 1)

        if next_clust > 3:
            return 0 
        y = self.centroids_lkp.ix[next_clust]

        return self._get_dist(x, y)


    def dist_centroid(self, x):
        y = self.centroids_lkp.ix[x['cluster_name']]
        return self._get_dist(x, y) 


    def get_distance_score(self, x):
        cx = self.centroids_lkp.ix[x['cluster_name']]
        next_clust = x['cluster_name'] + 1
        if next_clust > 3:
            return 0 
        cy = self.centroids_lkp.ix[next_clust]

        b = self._get_dist(cx, cy)
        a = self._get_dist(x, cy)

        return a / b



    def predict(self, x):
        label = self.model.predict((
            x['group_size'],
            x['margin_total'],
            x['n_items'],
            x['total_bill']
        ))[0]
        return self.label_map[label]