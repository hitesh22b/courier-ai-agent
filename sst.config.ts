/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "ai-project",
      removal: input?.stage === "production" ? "retain" : "remove",
      protect: ["production"].includes(input?.stage),
      home: "aws",
    };
  },
  async run() {
    const customerCareApi = new sst.aws.ApiGatewayV2("CustomerCareApi");

    customerCareApi.route("POST /ticket", "src/customer-care.handler");

    const agent = new sst.aws.ApiGatewayV2("Agent");
    agent.route("POST /agent", {
      handler: "src/python/agent.handler",
      runtime: "python3.11"
    });
  },
});
