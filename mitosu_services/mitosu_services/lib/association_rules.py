import pickle

class AssociationRules():
    def __init__(self, rules_path):

        with open(rules_path, "r") as f:
            self.rules = pickle.load(f)


    def matched_rules(self, items):
        items = set(items)
        rules = self.rules[self.rules['right'].apply(
                    lambda x : not bool(len(x - items)))
                ]
        return rules