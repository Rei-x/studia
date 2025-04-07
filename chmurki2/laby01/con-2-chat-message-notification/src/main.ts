import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app/app.module';
import { ChatMessageSentEvent } from 'src/domain/ChatMessageSentEvent';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.RMQ,
      options: {
        urls: [process.env.RABBIT_MQ_URL ?? ''],
        queue: ChatMessageSentEvent.name,
      },
    },
  );

  await app.listen();
}
void bootstrap();
