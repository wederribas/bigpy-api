def parse_as_graphene_object(id, aggregator, results, graphql_obj_instance):
    results_as_obj_list = []

    for odict in results:
        for key, value in odict.items():
            if key == '_id':
                attribute = value[id]

            if key == aggregator:
                agg = value

        result = graphql_obj_instance(attribute, agg)
        results_as_obj_list.append(result)

    return results_as_obj_list
