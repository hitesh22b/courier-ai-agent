import json
import requests
from strands import Agent, tool
from sst import Resource

SYSTEM_PROMPT = """You are a courier company assistant that can help customers track their packages and create support tickets

If a customer wants to book their travel, assist them with flight options for their destination and provide them with information about the weather.

Use the support_ticket tool to create customer support ticket.
Use the track_package tool to track customer packages.

Provide the users with a friendly customer support response.
"""

@tool
def track_package(package_id: str = None):
    """
    Track a package using the package ID
    Args:
        package_id: The ID of the package to track
    """
    if not package_id:
        return {"error": "Missing package_id"}

    try:
        # Get the track API URL from SST resources
        track_api_url = Resource.TrackApi.url
        
        # Make a POST request to the track API
        response = requests.post(
            f"{track_api_url}/track",
            headers={"Content-Type": "application/json"},
            json={"package_id": package_id},
            timeout=10
        )
        
        if response.status_code == 200:
            tracking_info = response.json()
            return {
                "success": True,
                "package_id": package_id,
                "tracking_info": tracking_info
            }
        else:
            return {
                "error": f"Failed to track package. Status: {response.status_code}",
                "package_id": package_id
            }
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout while tracking package", "package_id": package_id}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}", "package_id": package_id}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "package_id": package_id}


def handler(event, _context) -> dict:
    try:
        # Get the prompt from the event
        prompt = "Where is my package?"
        
        travel_agent = Agent(
            model="apac.amazon.nova-micro-v1:0",
            system_prompt=SYSTEM_PROMPT,
            tools=[track_package]  # Register the tool with the agent
        )
        
        response = travel_agent(prompt)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': str(response),
                'prompt': prompt
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }

