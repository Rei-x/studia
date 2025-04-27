import { CommandHandler, ICommandHandler, EventBus } from '@nestjs/cqrs';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Recording } from 'src/domain/entities/recording.entity';
import { Inject, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { StartRecordingCommand } from '../../domain/commands/start-recording.command';
import { RecordingCompletedEvent } from 'src/domain/events/recording-completed.event';

@CommandHandler(StartRecordingCommand)
export class StartRecordingHandler
  implements ICommandHandler<StartRecordingCommand>
{
  private readonly logger = new Logger(StartRecordingHandler.name);

  constructor(
    @InjectRepository(Recording)
    private recordingRepository: Repository<Recording>,
    @Inject('RABBIT_MQ_SERVICE') private readonly client: ClientProxy,
    private readonly eventBus: EventBus,
  ) {}

  async execute(command: StartRecordingCommand): Promise<string> {
    const { meetingId, title } = command;

    this.logger.log(`Starting recording for meeting: ${title} (${meetingId})`);

    // Create recording record in the database
    const recording = this.recordingRepository.create({
      meetingId,
      recordingUrl: '', // Will be populated when recording is complete
      durationSeconds: 0, // Will be updated when recording is complete
      status: 'in_progress',
    });

    const savedRecording = await this.recordingRepository.save(recording);

    this.logger.log(`Started recording for meeting ID: ${recording.meetingId}`);

    // Mock recording for 5-15 seconds
    const recordingDuration = Math.floor(Math.random() * 10) + 5;

    setTimeout(() => {
      void this.completeRecording(recording.id, recordingDuration);
    }, recordingDuration * 1000);

    return savedRecording.id;
  }

  private async completeRecording(
    recordingId: string,
    durationSeconds: number,
  ): Promise<void> {
    const recording = await this.recordingRepository.findOne({
      where: { id: recordingId },
    });

    if (!recording) {
      this.logger.error(`Recording with ID ${recordingId} not found`);
      return;
    }

    recording.status = 'completed';
    recording.durationSeconds = durationSeconds;
    recording.recordingUrl = `https://recordings.example.com/${recording.meetingId}/${recordingId}.mp4`;

    await this.recordingRepository.save(recording);

    this.logger.log(
      `Completed recording for meeting ID: ${recording.meetingId}, duration: ${durationSeconds}s`,
    );

    const event = new RecordingCompletedEvent(
      recording.id,
      recording.meetingId,
      recording.recordingUrl,
      recording.durationSeconds,
    );

    this.eventBus.publish(event);
    this.client.emit(RecordingCompletedEvent.name, event.serialize());

    this.logger.log(
      `Dispatched recording completed event for recording ID: ${recording.id}`,
    );
  }
}
