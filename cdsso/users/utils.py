from cdsso.utils.graphql.queries import GraphQLResponse, make_cdweb_query


def update_user_on_codedevils_website(user_data: dict) -> GraphQLResponse:
    """
    Updates the user with the corresponding user data on the CodeDevils website via a GraphQL query.

        :param user_data: The fields to update the user with. This must contain the `username` attribute
            or an `AttributeError` will be raised.
        :return: The GraphQL response of the query as a tuple.
    """
    if not user_data or "username" not in user_data:
        raise AttributeError("Missing attribute: username")

    attributes = []
    for attribute in user_data.keys():
        attributes.append(attribute)

    mutation = """mutation($user: UserSerializerMutationInput!) {
        updateUser(input: $user) {
            %s
            errors {
                field
                messages
            }
        }
    }"""
    variables = {"user": user_data}
    attributes = "\n".join(attributes)
    return make_cdweb_query(query=mutation % attributes, variables=variables)
