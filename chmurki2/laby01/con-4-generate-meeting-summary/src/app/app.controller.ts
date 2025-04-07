import { Controller } from '@nestjs/common';
import { AppService } from './app.service';
import { EventPattern } from '@nestjs/microservices';
import { MeetingTranscribedEvent } from 'src/domain/MeetingTranscribedEvent';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @EventPattern(MeetingTranscribedEvent.name)
  summarizeMeeting(data: string) {
    this.appService.summarizeMeeting(MeetingTranscribedEvent.deserialize(data));
  }
}
