import { Inject, Injectable, Logger } from '@nestjs/common';
import type { ClientProxy } from '@nestjs/microservices';
import { Cron } from '@nestjs/schedule';
import { MeetingEndedEvent as MeetingEndEvent } from 'src/domain/MeetingEndedEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  @Cron('* * * * * *')
  endMeeting() {
    if (Math.random() > 0.9) {
      this.logger.log('Meeting end event sent');
      this.client.emit(
        MeetingEndEvent.name,
        new MeetingEndEvent('meetingId', new Date()).serialize(),
      );
    }
  }
}
