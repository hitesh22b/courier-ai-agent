export async function handler() {
  return {
    statusCode: 200,
    body: JSON.stringify({
        id: "12345",
        src: "Bangalore",
        dest: "Mumbai",
        status: "In Progress",
        reachedAt: "Bangalore Office",
        updatedAt: new Date().toISOString()
    }),
  };
}