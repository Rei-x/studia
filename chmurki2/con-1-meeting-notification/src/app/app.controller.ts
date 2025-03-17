import { Controller } from '@nestjs/common';
import { AppService } from './app.service';
import { EventPattern } from '@nestjs/microservices';
import { MeetingStartedEvent } from 'src/domain/MeetingStartedEvent';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @EventPattern(MeetingStartedEvent.name)
  async getHello(data: string) {
    await this.appService.handleMeetingStartedEvent(
      MeetingStartedEvent.deserialize(data),
    );
  }
}
