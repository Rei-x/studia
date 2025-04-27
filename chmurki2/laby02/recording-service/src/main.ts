import { NestFactory } from '@nestjs/core';
import { Logger } from '@nestjs/common';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';
import { AppModule } from './app/app.module';
import { MeetingCreatedEvent } from 'src/domain/MeetingCreatedEvent';

async function bootstrap() {
  const logger = new Logger('Main');
  const app = await NestFactory.create(AppModule);

  const configService = app.get(ConfigService);
  const rabbitMqUrl = configService.getOrThrow<string>('RABBIT_MQ_URL');

  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.RMQ,
    options: {
      urls: [rabbitMqUrl],
      queue: MeetingCreatedEvent.name,
    },
  });

  await app.startAllMicroservices();

  await app.listen(3001);
  logger.log(`Notification service is running on port 3001`);
}

bootstrap();
