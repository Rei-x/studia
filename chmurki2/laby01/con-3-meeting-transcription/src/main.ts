import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app/app.module';
import { MeetingEndedEvent } from 'src/domain/MeetingEndedEvent';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.RMQ,
      options: {
        urls: [process.env.RABBIT_MQ_URL ?? ''],
        queue: MeetingEndedEvent.name,
      },
    },
  );

  await app.listen();
}
void bootstrap();
