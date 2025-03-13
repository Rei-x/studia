import amqp from "amqplib";
import { config } from "./config";
import type { BaseEvent } from "../domain/BaseEvent";
import { VideoRecordingCompletedEvent } from "../domain/VideoRecordingCompletedEvent";
import { logger } from "./logger";

const connection = await amqp.connect(config.RABBIT_MQ_URL);

const channel = await connection.createChannel();

const { queue } = await channel.assertQueue("hello");

const sendEvent = async (message: BaseEvent) => {
  logger.info({
    message: "Sending event",
    event: message,
    queue,
  });

  channel.sendToQueue(queue, Buffer.from(message.serialize()));
};

setInterval(() => {
  const eventId = Math.floor(Math.random() * 100000);
  sendEvent(
    new VideoRecordingCompletedEvent(
      `http://example.com/${eventId}-recording.mp4`
    )
  );
}, 3000);
