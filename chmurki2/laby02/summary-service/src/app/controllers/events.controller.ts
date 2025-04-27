import { Controller, Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { EventPattern, Payload } from '@nestjs/microservices';
import { TranscriptionGeneratedEvent } from 'src/domain/events/transcription-generated.event';
import { GenerateSummaryCommand } from 'src/domain/commands/generate-summary.command';

@Controller()
export class EventsController {
  private readonly logger = new Logger(EventsController.name);

  constructor(private readonly commandBus: CommandBus) {}

  @EventPattern(TranscriptionGeneratedEvent.name)
  async handleTranscriptionGenerated(@Payload() data: string) {
    this.logger.log(`Transcription generated event received`);
    const event = TranscriptionGeneratedEvent.deserialize(data);

    this.logger.log(
      `Generating summary for meeting ${event.meetingId}, recording ID: ${event.recordingId}`,
    );

    await this.commandBus.execute(
      new GenerateSummaryCommand(
        event.meetingId,
        event.recordingId,
        event.transcriptionUrl,
      ),
    );
  }
}
