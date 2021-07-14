import * as express from "express";
import * as helmet from "helmet";
import * as cors from "cors";
import * as swagger from "swagger-express-ts";
import { CommandBus } from "@tshio/command-bus";
import { QueryBus } from "@tshio/query-bus";
import { MiddlewareType } from "../shared/middleware-type/middleware.type";
import { NotFoundError } from "../errors/not-found.error";
import swaggerExpressOptions from "../tools/swagger";

export interface AppDependencies {
  router: express.Router;
  errorHandler: MiddlewareType;
  commandBus: CommandBus;
  queryBus: QueryBus;
  resolvers: any;
}

function createApp({ router, errorHandler, commandBus, queryBus, resolvers }: AppDependencies) {

  const app = express();

  app.use(cors());
  app.use(helmet());
  app.use(express.json());

  app.get("/health", (req, res) => {
    res.status(200).json({
      status: "ok",
    });
  });

  app.use("/api-docs", express.static("../swagger"));
  app.use("/api-docs/swagger/assets", express.static("../node_modules/swagger-ui-dist"));
  app.use(swagger.express(swaggerExpressOptions));
  app.use("/api", router);

  app.use("*", (req, res, next) => next(new NotFoundError("Page not found")));
  app.use(errorHandler);

  return app;
}

export { createApp };
