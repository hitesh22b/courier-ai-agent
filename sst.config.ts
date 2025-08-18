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

    const trackApi = new sst.aws.ApiGatewayV2("TrackApi");

    trackApi.route("POST /track", "src/track-status.handler");

    const pythonFunction = new sst.aws.Function("PythonHelloWorld", {
      handler: "python_functions/src/python_functions/hello.handler",
      runtime: "python3.12",
      url: true,
      link: [trackApi],
       permissions: [
        {
          actions: [
            "bedrock:InvokeModel",
            "bedrock:InvokeModelWithResponseStream"
          ],
          resources: [
            "arn:aws:bedrock:*::foundation-model/amazon.nova-micro-v1:0",
            "arn:aws:bedrock:ap-south-1:*:inference-profile/apac.amazon.nova-micro-v1:0"
          ]
        }
      ]
    });

    return {
      customerCareApi: customerCareApi.url,
      trackApi: trackApi.url,
      pythonFunction: pythonFunction.url,
    };
  },
});
