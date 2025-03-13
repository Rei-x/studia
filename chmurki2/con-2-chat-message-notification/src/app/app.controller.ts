import { Controller } from '@nestjs/common';
import { AppService } from './app.service';
import { EventPattern } from '@nestjs/microservices';
import { ChatMessageSentEvent } from 'src/domain/ChatMessageSentEvent';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @EventPattern(ChatMessageSentEvent.name)
  getHello(data: string) {
    this.appService.handleChatMessageSentEvent(
      ChatMessageSentEvent.deserialize(data),
    );
  }
}
