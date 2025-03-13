import "dotenv/config";
import assert from "node:assert";

const RABBIT_MQ_URL = process.env.RABBIT_MQ_URL;
assert(RABBIT_MQ_URL, "RABBIT_MQ_URL is required");

const config = {
  RABBIT_MQ_URL,
};

export { config };
