"""Main entry point
"""
import pandas

from pyramid.config import Configurator
from mitosu_services.lib.cluster_model import ClusterModel
from mitosu_services.lib.association_rules import AssociationRules


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")


    # Load cluster model
    model = settings['mitosu.cluster_model']
    config.registry.cluster_model = ClusterModel(model)

    # Load Association Rules
    rules = settings['mitosu.association_rules']
    config.registry.association_rules = AssociationRules(rules)

    # Items
    config.registry.items = pandas.read_csv(
        settings['mitosu.items']
    )


    config.scan("mitosu_services.views")
    return config.make_wsgi_app()
