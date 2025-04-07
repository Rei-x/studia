import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app/app.module';
import { MeetingTranscribedEvent } from 'src/domain/MeetingTranscribedEvent';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.RMQ,
      options: {
        urls: [process.env.RABBIT_MQ_URL ?? ''],
        queue: MeetingTranscribedEvent.name,
      },
    },
  );

  await app.listen();
}
void bootstrap();
