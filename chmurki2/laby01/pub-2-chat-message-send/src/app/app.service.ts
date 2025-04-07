import { Inject, Injectable, Logger } from '@nestjs/common';
import type { ClientProxy } from '@nestjs/microservices';
import { Cron } from '@nestjs/schedule';
import { ChatMessageSentEvent } from 'src/domain/ChatMessageSentEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  @Cron('* * * * * *')
  sendChatMessage() {
    if (Math.random() > 0.9) {
      this.logger.log('Chat message event sent');
      this.client.emit(
        ChatMessageSentEvent.name,
        new ChatMessageSentEvent('meetingId', 'Hello!').serialize(),
      );
    }
  }
}
