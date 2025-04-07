import { Inject, Injectable, Logger } from '@nestjs/common';
import type { ClientProxy } from '@nestjs/microservices';
import { Cron } from '@nestjs/schedule';
import { MeetingStartedEvent } from 'src/domain/MeetingStartedEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  @Cron('*/5 * * * * *')
  startMeeting() {
    this.logger.log('Meeting started event sent');
    this.client.emit(
      MeetingStartedEvent.name,
      new MeetingStartedEvent('meetingId', new Date()).serialize(),
    );
  }
}
