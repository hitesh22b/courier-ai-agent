import json
import requests
from strands import Agent, tool
from sst import Resource

SYSTEM_PROMPT = """You are a courier company assistant that can help customers track their packages and create support tickets

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
        
        # Make a GET request to the track API with package_id in path
        response = requests.get(
            f"{track_api_url}/track/{package_id}",
            headers={"Content-Type": "application/json"},
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


@tool
def create_support_ticket(email: str = None, phoneNo: str = None, issueDescription: str = None, packageId: str = None):
    """
    Create a customer support ticket
    Args:
        email: Customer's email address
        phoneNo: Customer's phone number
        issueDescription: Description of the issue
        packageId: Related package ID (optional)
    """
    if not email or not phoneNo or not issueDescription:
        return {"error": "Missing required fields: email, phoneNo, issueDescription"}
    
    try:
        # Get the customer care API URL from SST resources
        customer_care_url = Resource.CustomerCareApi.url
        
        # Prepare the request payload
        payload = {
            "email": email,
            "phoneNo": phoneNo,
            "issueDescription": issueDescription,
            "packageId": packageId or "N/A"  # Use N/A if no package ID provided
        }
        
        # Make a POST request to create support ticket
        response = requests.post(
            f"{customer_care_url}/ticket",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 201:
            ticket_info = response.json()
            return {
                "success": True,
                "message": "Support ticket created successfully",
                "ticket": ticket_info.get("ticket", {})
            }
        else:
            error_info = response.json() if response.headers.get('content-type') == 'application/json' else {"error": "Unknown error"}
            return {
                "error": f"Failed to create support ticket. Status: {response.status_code}",
                "details": error_info
            }
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout while creating support ticket"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def handler(event, _context) -> dict:
    try:    
        if 'body' in event:
            try:
                # Parse JSON body if it exists
                if isinstance(event['body'], str):
                    body = json.loads(event['body'])
                else:
                    body = event['body']
                
                # Extract prompt from body
                prompt = body.get('prompt', prompt)
            except (json.JSONDecodeError, TypeError):
                # If body parsing fails, check if body is directly the prompt
                if isinstance(event['body'], str):
                    prompt = event['body']
        
        # Also check for direct prompt field in event (for Lambda test console)
        elif 'prompt' in event:
            prompt = event['prompt']
        
        travel_agent = Agent(
            model="apac.amazon.nova-micro-v1:0",
            system_prompt=SYSTEM_PROMPT,
            tools=[track_package, create_support_ticket]  # Register both tools with the agent
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

