import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';

import { TypeOrmModule } from '@nestjs/typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { databaseConfig } from 'src/app/config/database.config';

import { MeetingsModule } from '../web-api/meetings/meetings.module';
import { CqrsModule } from '@nestjs/cqrs';
import { CreateMeetingHandler } from 'src/app/handlers/create-meeting.handler';
import { GetAllMeetingsHandler } from 'src/app/handlers/get-all-meetings.handler';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { MeetingCreatedEvent } from 'src/domain/meeting-created.event';
import { ScheduleModule } from '@nestjs/schedule';
import { MeetingStarter } from 'src/app/services/meeting-starter';
import { DispatchMeetingStartedHandler } from 'src/app/handlers/dispatch-meeting-started.handler';
import { GetMeetingsToStartHandler } from 'src/app/handlers/get-meetings-to-start.handler';

@Module({
  imports: [
    ConfigModule.forRoot(),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) =>
        databaseConfig(configService.getOrThrow<string>('DATABASE_URL')),
    }),
    ClientsModule.registerAsync([
      {
        imports: [ConfigModule],
        name: 'RABBIT_MQ_SERVICE',
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.getOrThrow<string>('RABBIT_MQ_URL')],
            queue: MeetingCreatedEvent.name,
          },
        }),
        inject: [ConfigService],
      },
    ]),
    ScheduleModule.forRoot(),
    TypeOrmModule.forFeature([Meeting]),
    CqrsModule,
    MeetingsModule,
  ],
  providers: [
    CreateMeetingHandler,
    GetAllMeetingsHandler,
    DispatchMeetingStartedHandler,
    GetMeetingsToStartHandler,
    MeetingStarter,
  ],
  exports: [],
})
export class AppModule {}
