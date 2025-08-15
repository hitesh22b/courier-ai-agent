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

    const pythonFunction = new sst.aws.Function("PythonHelloWorld", {
      handler: "python_functions/src/python_functions/hello.handler",
      runtime: "python3.12",
      url: true,
    });

    return {
      customerCareApi: customerCareApi.url,
      pythonFunction: pythonFunction.url,
    };
  },
});
