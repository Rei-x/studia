import { Controller, Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { EventPattern, Payload } from '@nestjs/microservices';
import { RecordingCompletedEvent } from 'src/domain/events/recording-completed.event';
import { ProcessRecordingCommand } from 'src/domain/commands/process-recording.command';

@Controller()
export class EventsController {
  private readonly logger = new Logger(EventsController.name);

  constructor(private readonly commandBus: CommandBus) {}

  @EventPattern(RecordingCompletedEvent.name)
  async handleRecordingCompleted(@Payload() data: string) {
    this.logger.log(`Recording completed event received`);
    const event = RecordingCompletedEvent.deserialize(data);

    this.logger.log(
      `Processing recording for meeting ${event.meetingId}, recording ID: ${event.recordingId}`,
    );

    await this.commandBus.execute(
      new ProcessRecordingCommand(
        event.recordingId,
        event.meetingId,
        event.recordingUrl,
        event.durationSeconds,
      ),
    );
  }
}
