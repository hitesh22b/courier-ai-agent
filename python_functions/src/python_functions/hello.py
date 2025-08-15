def handler(event, context):
    """
    Python Lambda handler that returns Hello World
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "Hello World from Pyth9on."
    }
