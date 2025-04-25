import { Controller } from '@nestjs/common';
import { AppService } from './app.service';
import { EventPattern } from '@nestjs/microservices';
import { MeetingEndedEvent } from 'src/domain/MeetingEndedEvent';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @EventPattern(MeetingEndedEvent.name)
  async transcribeMeetingData(data: string) {
    await this.appService.transcribeMeeting(
      MeetingEndedEvent.deserialize(data),
    );
  }
}
