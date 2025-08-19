import json
import requests
import boto3
import os
from strands import Agent, tool
from sst import Resource

ddb = boto3.resource('dynamodb')
agent_state_table = ddb.Table(os.environ['SESSIONS_TABLE'])

def get_session_history(user_id):
    ddb_response = agent_state_table.get_item(Key={'sessionID': user_id})
    item = ddb_response.get('Item')
    if item:
        messages=json.loads(item['state'])
    else:
        messages = []

    print(f"messages={messages}")
    return messages

def update_session_history(user_id, messages):
    agent_state_table.put_item(Item={
        'sessionID': user_id,
        'state': json.dumps(messages),
    })

SYSTEM_PROMPT = """You are a helpful AI assistant for a courier and package delivery company. You help customers with:

1. **Package Tracking**: Use the track_package tool to look up package status and delivery information using tracking numbers
2. **Customer Support**: Use the create_support_ticket tool to create support tickets for issues, complaints, or inquiries  
3. **Company Policies**: Use the search_knowledge_base tool to answer questions about delivery policies, shipping rates, restrictions, and procedures

Always be polite, professional, and helpful. If you need more information to assist the customer, ask clarifying questions. For package tracking, always use the exact tracking number provided. For support tickets, collect all necessary details including contact information.

When answering policy questions, search the knowledge base first to provide accurate and up-to-date information about company policies and procedures.
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


@tool
def search_knowledge_base(query: str = None):
    """
    Search the company knowledge base for policies, procedures, and information
    Args:
        query: The search query to find relevant information
    """
    if not query:
        return {"error": "Missing query parameter"}

    try:
        # Get the knowledge base API URL from SST resources
        knowledge_base_url = Resource.KnowledgeBaseApi.url
        
        # Prepare the request payload
        payload = {
            "query": query
        }
        
        # Make a POST request to search the knowledge base
        response = requests.post(
            f"{knowledge_base_url}/search",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            search_results = response.json()
            return {
                "success": True,
                "query": query,
                "results": search_results
            }
        else:
            error_info = response.json() if response.headers.get('content-type') == 'application/json' else {"error": "Unknown error"}
            return {
                "error": f"Failed to search knowledge base. Status: {response.status_code}",
                "details": error_info
            }
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout while searching knowledge base"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def handler(event, _context) -> dict:
    try:
        # Initialize default values
        prompt = "How can I help you today?"
        user_id = "anonymous"
        
        if 'body' in event:
            try:
                # Parse JSON body if it exists
                if isinstance(event['body'], str):
                    body = json.loads(event['body'])
                else:
                    body = event['body']
                
                # Extract prompt and user_id from body
                prompt = body.get('prompt', prompt)
                user_id = body.get('user_id', body.get('userId', user_id))
                
            except (json.JSONDecodeError, TypeError):
                # If body parsing fails, check if body is directly the prompt
                if isinstance(event['body'], str):
                    prompt = event['body']
        
        # Also check for direct fields in event (for Lambda test console)
        elif 'prompt' in event:
            prompt = event['prompt']
        
        if 'user_id' in event:
            user_id = event['user_id']
        elif 'userId' in event:
            user_id = event['userId']
        
        session_history = get_session_history(user_id)
        travel_agent = Agent(
            model="apac.amazon.nova-micro-v1:0",
            system_prompt=SYSTEM_PROMPT,
            tools=[track_package, create_support_ticket, search_knowledge_base],  # Register all three tools with the agent
            messages=session_history
        )
        
        response = travel_agent(prompt)
        
        # Update session history with new messages after the conversation
        update_session_history(user_id, travel_agent.messages)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': str(response),
                'prompt': prompt,
                'user_id': user_id
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

