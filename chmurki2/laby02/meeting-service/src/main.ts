import { NestFactory } from '@nestjs/core';
import { AppModule } from './app/app.module';
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
        enableImplicitConversion: true,
      },
    }),
  );

  await app.startAllMicroservices();
  await app.listen(3000);

  console.log(`Application is running on: http://localhost:3000`);
}
void bootstrap();
