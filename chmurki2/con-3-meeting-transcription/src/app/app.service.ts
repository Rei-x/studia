import { Inject, Injectable, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import type { ChatMessageSentEvent } from 'src/domain/MeetingEndedEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  transcribeMeeting(data: ChatMessageSentEvent) {
    this.logger.log('Chat message sent event received', data);
  }
}
