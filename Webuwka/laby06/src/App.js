import { createServer } from "node:http";
import { createYoga } from "graphql-yoga";
import { schema } from "./schema.js";

// Create a Yoga instance with a GraphQL schema
const yoga = createYoga({ schema });

// Pass it into a server to hook into request handlers
const server = createServer(yoga);

// Start the server
const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
  console.info(`🚀 Server is running on http://localhost:${PORT}/graphql`);
  console.info("Try the demo query: { demo }");
});
