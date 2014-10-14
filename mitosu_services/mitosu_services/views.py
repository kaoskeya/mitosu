""" Cornice services.
"""
import json
from cornice import Service
import pandas


cors_policy = {'origins': ('*',),
              'credentials': True}

dss = Service(name = 'dss', path = '/dss',
              description = "Decision Suppport",
              cors_policy = cors_policy)

@dss.post()
def get_decision_support(request):
    cm = request.registry.cluster_model
    ar = request.registry.association_rules
    item_df = request.registry.items

    cluster_map = {
        1 : "Silver",
        2 : "Gold",
        3 : "Platinum"
    }

    seg_discount = {
        1 : 5,
        2 : 10,
        3 : 5
    }


    payload = json.loads(request.body)

    item_ids = map(lambda x: x['item'], payload['items'])

    item_qty = map(lambda x: x['quantity'], payload['items'])
    item_qty_map = dict(zip(item_ids, item_qty))

    # Item Recommendations
    matched = ar.matched_rules(item_ids)
    new_items = list(set(matched['left'].unique()) - set(item_ids))
    new_items = filter(lambda x: x not in ['i55', 'i56'], new_items)

    # Customer Type
    items = item_df[item_df['Id'].isin(item_ids)]
    items["quantity"] = items['Id'].apply(lambda x: item_qty_map[x])

    x = {
        "group_size" : payload['group_size'],
        "margin_total" : sum(items['Margin'] * items['Price'] * items["quantity"]),
        "n_items" : len(items),
        "total_bill" : sum(items['Price'] * items["quantity"])
    }

    x['cluster_name'] = cm.predict(x)

    distance_score = cm.get_distance_score(x)

    discount = 0.0
    if distance_score < 1:
        discount = seg_discount[x['cluster_name']]

    resp = {
        "item_recommendations" : new_items,
        "customer_segment" : cluster_map[x['cluster_name']],
        "discount" : discount,
        "discount_score" : distance_score
    }

    print resp

    return resp 