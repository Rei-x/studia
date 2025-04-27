import { Controller, Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { EventPattern } from '@nestjs/microservices';
import { MeetingStartedEvent } from 'src/domain/events/meeting-started.event';
import { StartRecordingCommand } from 'src/domain/commands/start-recording.command';

@Controller()
export class EventsController {
  private readonly logger = new Logger(EventsController.name);

  constructor(private readonly commandBus: CommandBus) {}

  @EventPattern(MeetingStartedEvent.name)
  async handleMeetingStarted(data: string): Promise<void> {
    this.logger.log(`Received meeting started event: ${data}`);

    const meetingStartedEvent = MeetingStartedEvent.deserialize(data);

    this.logger.log(
      `Processing meeting started event for meeting: ${meetingStartedEvent.title} (${meetingStartedEvent.meetingId})`,
    );

    await this.commandBus.execute(
      new StartRecordingCommand(
        meetingStartedEvent.meetingId,
        meetingStartedEvent.title,
      ),
    );
  }
}
