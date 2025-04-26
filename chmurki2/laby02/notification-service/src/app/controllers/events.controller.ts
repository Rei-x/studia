import { Controller, Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { EventPattern, Payload } from '@nestjs/microservices';
import { MeetingCreatedEvent } from '../../domain/MeetingCreatedEvent';
import { SendNotificationCommand } from '../../domain/commands/send-notification.command';

@Controller()
export class EventsController {
  private readonly logger = new Logger(EventsController.name);

  constructor(private readonly commandBus: CommandBus) {}

  @EventPattern(MeetingCreatedEvent.name)
  async handleMeetingCreated(@Payload() data: any) {
    const event = MeetingCreatedEvent.deserialize(data);
    this.logger.log(`Meeting created event received: ${event.meetingId}`);

    const { meetingId, title, startTime, endTime, participantEmails } = event;

    if (!participantEmails || participantEmails.length === 0) {
      this.logger.log('No participants to notify');
      return;
    }

    await this.commandBus.execute(
      new SendNotificationCommand(
        meetingId,
        title,
        startTime,
        participantEmails,
        endTime,
      ),
    );
  }
}
