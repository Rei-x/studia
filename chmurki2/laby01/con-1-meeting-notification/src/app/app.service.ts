import { Inject, Injectable, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import type { MeetingStartedEvent } from 'src/domain/MeetingStartedEvent';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  constructor(@Inject('RABBIT_MQ_SERVICE') private client: ClientProxy) {}

  async handleMeetingStartedEvent(data: MeetingStartedEvent) {
    this.logger.log('Meeting started event received', data);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    this.logger.log('Meeting started event processe', data);
  }
}
