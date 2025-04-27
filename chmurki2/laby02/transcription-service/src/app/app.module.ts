import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CqrsModule } from '@nestjs/cqrs';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { databaseConfig } from './config/database.config';

import { Transcription } from 'src/domain/entities/transcription.entity';
import { ProcessRecordingHandler } from './handlers/process-recording.handler';
import { EventsController } from './controllers/events.controller';
import { TranscriptionGeneratedEvent } from 'src/domain/events/transcription-generated.event';

const CommandHandlers = [ProcessRecordingHandler];
const Controllers = [EventsController];

@Module({
  imports: [
    ConfigModule.forRoot(),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) =>
        databaseConfig(configService.getOrThrow<string>('DATABASE_URL')),
    }),
    TypeOrmModule.forFeature([Transcription]),
    ClientsModule.registerAsync([
      {
        imports: [ConfigModule],
        name: 'RABBIT_MQ_SERVICE',
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.getOrThrow<string>('RABBIT_MQ_URL')],
            queue: TranscriptionGeneratedEvent.name,
            queueOptions: {
              durable: true,
            },
          },
        }),
        inject: [ConfigService],
      },
    ]),
    CqrsModule,
  ],
  controllers: [...Controllers],
  providers: [...CommandHandlers],
})
export class AppModule {}
