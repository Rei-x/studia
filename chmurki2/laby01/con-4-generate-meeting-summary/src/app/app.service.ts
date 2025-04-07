import { Inject, Injectable, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import type { MeetingTranscribedEvent } from 'src/domain/MeetingTranscribedEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  summarizeMeeting(data: MeetingTranscribedEvent) {
    this.logger.log('Summarizing meeting', data);
  }
}
