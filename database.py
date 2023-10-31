from neo4j import GraphDatabase, Driver

URI = "neo4j+s://e478977f.databases.neo4j.io"
AUTH = ("neo4j", "_T8z-J6M7BJxAL0QYGtaUQrX1YMSFE23J9N1BlgNEUY")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties
