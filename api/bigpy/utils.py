def parse_results_as_graphe_object(results, id, graphql_obj_instance):
    results_as_obj_list = []

    for odict in results:
        for key, value in odict.items():
            if key == '_id':
                attribute = value[id]

            if key == 'count':
                count = value

        result = graphql_obj_instance(attribute, count)
        results_as_obj_list.append(result)

    return results_as_obj_list
