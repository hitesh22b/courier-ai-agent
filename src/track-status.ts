import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

export async function handler(event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  try {
    const packages = ["12345", "23456", "34567"];
    
    // Extract package ID from path parameters
    const packageId = event.pathParameters?.packageId || event.pathParameters?.id;
    
    if (!packageId) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: "Missing package ID in path parameters"
        }),
      };
    }
    
    // Check if package ID exists in packages array
    if (!packages.includes(packageId)) {
      return {
        statusCode: 404,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error: "No such package found",
          package_id: packageId
        }),
      };
    }
    
    // Return tracking information for valid package
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: packageId,
        src: "Bangalore",
        dest: "Mumbai",
        status: "In Progress",
        reachedAt: "Bangalore Office",
        updatedAt: new Date().toISOString()
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