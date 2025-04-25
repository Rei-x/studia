import { Module } from '@nestjs/common';
import { MeetingsController } from './controllers/meetings.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { MeetingService } from 'src/app/services/meeting.service';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { MeetingTranscribedEvent } from 'src/domain/MeetingTranscribedEvent';
import { CqrsModule } from '@nestjs/cqrs';
import { CreateMeetingHandler } from 'src/app/handlers/create-meeting.handler';
import { GetAllMeetingsHandler } from 'src/app/handlers/get-all-meetings.handler';
import { MeetingApplicationService } from 'src/app/services/meeting-application.service';

const CommandHandlers = [CreateMeetingHandler];
const QueryHandlers = [GetAllMeetingsHandler];

@Module({
  imports: [
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
  ],
  controllers: [MeetingsController],
  providers: [
    MeetingService,
    MeetingApplicationService,
    ...CommandHandlers,
    ...QueryHandlers,
  ],
})
export class MeetingsModule {}
