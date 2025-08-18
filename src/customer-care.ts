import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

interface SupportTicketRequest {
  email: string;
  phoneNo: string;
  issueDescription: string;
  packageId: string;
}

export async function handler(event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  try {
    // Parse the request body
    if (!event.body) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: "Missing request body"
        }),
      };
    }

    let requestData: SupportTicketRequest;
    try {
      requestData = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    } catch (error) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: "Invalid JSON in request body"
        }),
      };
    }

    // Validate required fields
    const { email, phoneNo, issueDescription, packageId } = requestData;
    
    if (!email || !phoneNo || !issueDescription || !packageId) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: "Missing required fields",
          required: ["email", "phoneNo", "issueDescription", "packageId"],
          provided: {
            email: !!email,
            phoneNo: !!phoneNo,
            issueDescription: !!issueDescription,
            packageId: !!packageId
          }
        }),
      };
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: "Invalid email format"
        }),
      };
    }

    // Generate a ticket ID (in real world, this would be from a database)
    const ticketId = `TK-${Date.now()}-${Math.random().toString(36).substr(2, 6).toUpperCase()}`;

    // Create support ticket (in real world, save to database)
    const supportTicket = {
      ticketId,
      email,
      phoneNo,
      issueDescription,
      packageId,
      status: "Open",
      priority: "Medium",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    // Return success response with ticket details
    return {
      statusCode: 201,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: "Support ticket created successfully",
        ticket: supportTicket
      }),
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        error: "Internal Server Error",
        message: error instanceof Error ? error.message : 'Unknown error'
      }),
    };
  }
}