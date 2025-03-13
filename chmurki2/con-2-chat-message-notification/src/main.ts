import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app/app.module';
import { MeetingStartedEvent } from 'src/domain/MeetingStartedEvent';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.RMQ,
      options: {
        urls: [process.env.RABBIT_MQ_URL ?? ''],
        queue: MeetingStartedEvent.name,
      },
    },
  );

  await app.listen();
}
void bootstrap();
