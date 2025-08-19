import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

export async function handler(event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  try {
    const body = JSON.parse(event.body || '{}');
    const query = body.query;

    if (!query) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          error: 'Missing query parameter' 
        })
      };
    }

    // Mock knowledge base with common courier company policies
    const knowledgeBase: { [key: string]: string } = {
      "damaged packages": "If your package arrives damaged, we offer full replacement within 48 hours. Photo evidence required for claims over $100. Contact customer service with your tracking number and photos of the damage.",
      
      "delivery times": "Standard delivery: 3-5 business days within India. Express delivery: 1-2 business days. Same-day delivery available in major cities (Mumbai, Delhi, Bangalore, Chennai, Hyderabad). International deliveries take 7-14 business days.",
      
      "international shipping": "International deliveries take 7-14 business days. Additional customs fees may apply. Prohibited items include batteries, liquids, perishables, and hazardous materials. Maximum package weight is 30kg for international shipments.",
      
      "lost packages": "Lost packages are investigated within 24 hours. Full refund or replacement provided after 7-day investigation period. Track your claim through our customer portal or contact support with your tracking number.",
      
      "shipping costs": "Shipping costs depend on weight, distance, and delivery speed. Standard rates start at ₹50 for local delivery, ₹120 for interstate delivery. Express delivery adds 50% to standard rates. Same-day delivery available for ₹200 extra.",
      
      "package tracking": "You can track your package 24/7 using your tracking number on our website or mobile app. Real-time updates are provided at each checkpoint. SMS notifications are sent for major status changes.",
      
      "pickup services": "Free pickup available for packages over ₹500 value. Schedule pickup online or call customer service. Pickup available Monday-Saturday, 9 AM to 6 PM. Same-day pickup available in major cities.",
      
      "insurance claims": "Package insurance covers up to declared value (maximum ₹50,000). Claims must be filed within 30 days of delivery. Required documents: tracking number, photos of damage, purchase receipts, and insurance claim form.",
      
      "return policy": "Packages can be returned to sender if undelivered after 3 attempts. Return-to-sender charges apply. Customer can also request package hold at nearest hub for 7 days before return.",
      
      "prohibited items": "Prohibited items include: hazardous materials, flammable liquids, batteries (certain types), perishable food items, live animals, illegal substances, and items over 50kg. Contact support for specific item queries.",
      
      "customer support": "Customer support available 24/7. Phone: 1800-COURIER (1800-268-7437). Email: support@courier.com. Live chat available on website and mobile app. Average response time: 2 hours.",
      
      "holiday delivery": "Limited delivery services during national holidays. Express and same-day services may not be available. Standard delivery may be delayed by 1-2 days during festival seasons. Check holiday schedule on our website."
    };

    const lowerQuery = query.toLowerCase();
    let relevantInfo = "I don't have specific information about that topic. Please contact our customer support at 1800-COURIER (1800-268-7437) or email support@courier.com for detailed assistance.";
    let foundKey = "";

    // Search for relevant information
    for (const [key, value] of Object.entries(knowledgeBase)) {
      if (lowerQuery.includes(key) || key.includes(lowerQuery)) {
        relevantInfo = value;
        foundKey = key;
        break;
      }
    }

    // Additional fuzzy matching for common variations
    if (foundKey === "") {
      const fuzzyMatches: { [key: string]: string[] } = {
        "damaged packages": ["damage", "broken", "destroyed", "crushed"],
        "delivery times": ["how long", "delivery time", "when will", "how fast", "speed"],
        "international shipping": ["international", "overseas", "abroad", "foreign"],
        "lost packages": ["lost", "missing", "can't find", "disappeared"],
        "shipping costs": ["cost", "price", "charges", "fees", "rates", "how much"],
        "package tracking": ["track", "status", "where is", "location"],
        "pickup services": ["pickup", "collection", "collect"],
        "insurance claims": ["insurance", "claim", "compensation"],
        "return policy": ["return", "send back"],
        "prohibited items": ["prohibited", "restricted", "not allowed", "banned"],
        "customer support": ["support", "help", "contact", "phone", "email"],
        "holiday delivery": ["holiday", "festival", "christmas", "diwali"]
      };

      for (const [category, keywords] of Object.entries(fuzzyMatches)) {
        if (keywords.some(keyword => lowerQuery.includes(keyword))) {
          relevantInfo = knowledgeBase[category];
          foundKey = category;
          break;
        }
      }
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        relevant_docs: [relevantInfo],
        category: foundKey || "general",
        source: "company_policies"
      })
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        error: 'Internal Server Error',
        message: error instanceof Error ? error.message : 'Unknown error'
      })
    };
  }
}
