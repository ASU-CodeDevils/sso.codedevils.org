import json
import logging
from typing import Dict, Tuple

import requests
from django.conf import settings

logger = logging.getLogger()
GraphQLResponse = Tuple[bool, bool, Dict]


def make_cdweb_query(query: str, variables: dict = None) -> GraphQLResponse:
    """
    Makes a GraphQL query to the CodeDevils website.
    """
    return make_query(
        query=query,
        variables=variables,
        url=settings.CODEDEVILS_WEBSITE_GRAPHQL_URL,
        headers={"Authorization": f"Token {settings.CODEDEVILS_WEBSITE_API_KEY}"}
    )


def make_query(url: str, query: str, variables: dict = None, headers: dict = None) -> GraphQLResponse:
    """
    Constructs and sends a GraphQL query. The query returns a tuple with the status of the query,
    the status of a mutation (if any), and the data itself.

        :param query: The GraphQL-formatted query.
        :param variables: GraphQL variables (indicated within queries with the $ symbol).
        :param url: The GraphQL endpoint.
        :param headers: Additional headers. By default the content header is set to application/json.
    """
    # add json header by default
    query_header = {"Content": "application/json"}
    if headers:
        query_header.update(headers)

    data = {"query": query, "variables": json.dumps(variables)}
    response = requests.post(url, data=data, headers=query_header)
    status = response.status_code

    try:
        response = response.json()
    except Exception as e:
        logger.error(f"Error deserializing GraphQL query: {str(e)}")
        raise

    if status == 200 or status == 204:
        if response.get("errors", False):
            return False, False, response["errors"]
        elif response["data"].get("errors", False):
            return True, False, response["data"]
        else:
            return True, True, response["data"]
    else:
        error_message = response["errors"][0]["message"]
        raise Exception(f"Query failed to run by returning code of {status}: {error_message}")
