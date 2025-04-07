import { Inject, Injectable, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import type { MeetingEndedEvent } from 'src/domain/MeetingEndedEvent';
import { MeetingTranscribedEvent } from 'src/domain/MeetingTranscribedEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  async transcribeMeeting(data: MeetingEndedEvent) {
    this.logger.log('Transcribing meeting', data);

    await new Promise((res) => setTimeout(res, 2000));

    this.client.emit(
      MeetingTranscribedEvent.name,
      new MeetingTranscribedEvent(data.meetingId).serialize(),
    );
  }
}
