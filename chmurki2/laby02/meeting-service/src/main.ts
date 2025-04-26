import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app/app.module';
import { MeetingCreatedEvent } from 'src/domain/meeting-created.event';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  // Create a hybrid application that supports both HTTP and microservices
  const app = await NestFactory.create(AppModule);

  // Enable validation
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true, // Strip properties not in DTO
      transform: true, // Transform payloads to DTO instances
      forbidNonWhitelisted: true, // Throw errors if non-whitelisted properties are present
      transformOptions: {
        enableImplicitConversion: true, // Attempt to convert primitive types
      },
    }),
  );

  // Connect to RabbitMQ as a microservice
  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.RMQ,
    options: {
      urls: [process.env.RABBIT_MQ_URL ?? ''],
      queue: MeetingCreatedEvent.name,
    },
  });

  // Start both the microservice and HTTP application
  await app.startAllMicroservices();
  await app.listen(3000);

  console.log(`Application is running on: http://localhost:3000`);
}
void bootstrap();
