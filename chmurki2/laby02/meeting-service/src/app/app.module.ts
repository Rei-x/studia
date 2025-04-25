import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { MeetingTranscribedEvent } from 'src/domain/MeetingTranscribedEvent';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { databaseConfig } from 'src/app/config/database.config';
import { MeetingService } from './services/meeting.service';
import { MeetingsModule } from '../web-api/meetings/meetings.module';
import { CqrsModule } from '@nestjs/cqrs';
import { CreateMeetingHandler } from './handlers/create-meeting.handler';
import { GetAllMeetingsHandler } from './handlers/get-all-meetings.handler';

// Define handlers array for better organization
const CommandHandlers = [CreateMeetingHandler];
const QueryHandlers = [GetAllMeetingsHandler];

@Module({
  imports: [
    ConfigModule.forRoot(),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) =>
        databaseConfig(configService.getOrThrow<string>('DATABASE_URL')),
    }),
    TypeOrmModule.forFeature([Meeting]),
    ClientsModule.registerAsync([
      {
        imports: [ConfigModule],
        name: 'RABBIT_MQ_SERVICE',
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.getOrThrow<string>('RABBIT_MQ_URL')],
            queue: MeetingTranscribedEvent.name,
          },
        }),
        inject: [ConfigService],
      },
    ]),
    CqrsModule,
    MeetingsModule,
  ],
  controllers: [AppController],
  providers: [AppService, MeetingService, ...CommandHandlers, ...QueryHandlers],
  exports: [MeetingService],
})
export class AppModule {}
