import { CommandHandler, ICommandHandler, EventBus } from '@nestjs/cqrs';
import { ProcessRecordingCommand } from '../../domain/commands/process-recording.command';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Transcription } from 'src/domain/entities/transcription.entity';
import { Inject, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { TranscriptionGeneratedEvent } from 'src/domain/events/transcription-generated.event';
import { firstValueFrom } from 'rxjs';

@CommandHandler(ProcessRecordingCommand)
export class ProcessRecordingHandler
  implements ICommandHandler<ProcessRecordingCommand>
{
  private readonly logger = new Logger(ProcessRecordingHandler.name);

  constructor(
    @InjectRepository(Transcription)
    private transcriptionRepository: Repository<Transcription>,
    @Inject('RABBIT_MQ_SERVICE') private readonly client: ClientProxy,
    private readonly eventBus: EventBus,
  ) {}

  async execute(command: ProcessRecordingCommand): Promise<string> {
    const { recordingId, meetingId, recordingUrl, durationSeconds } = command;

    this.logger.log(`Downloading recording from ${recordingUrl}...`);
    await this.delay(1000);
    this.logger.log('Recording downloaded successfully');

    this.logger.log('Generating transcription...');
    await this.delay(2000);
    const transcriptionContent = this.generateMockTranscription();
    this.logger.log('Transcription generated successfully');

    this.logger.log('Uploading transcription to storage...');
    await this.delay(500);
    const transcriptionUrl = `https://example-storage.com/transcriptions/${recordingId}.txt`;
    this.logger.log(`Transcription uploaded to ${transcriptionUrl}`);

    // Save transcription to database
    const transcription = this.transcriptionRepository.create({
      recordingId,
      meetingId,
      transcriptionUrl,
      content: transcriptionContent,
    });
    const trans = await this.transcriptionRepository.save(transcription);

    // Create and emit event
    const event = new TranscriptionGeneratedEvent(
      meetingId,
      recordingId,
      transcriptionUrl,
      durationSeconds,
    );

    // Publish event internally and to message queue
    this.eventBus.publish(event);
    await firstValueFrom(
      this.client.emit(TranscriptionGeneratedEvent.name, event.serialize()),
    );

    this.logger.log(
      `Transcription completed for recording ID: ${recordingId}, meeting ID: ${meetingId}`,
    );

    return trans.id;
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private generateMockTranscription(): string {
    const phrases = [
      'Welcome to the meeting.',
      'Let me share my screen.',
      'Can everyone hear me?',
      "Let's discuss the project status.",
      'We need to address these issues.',
      'The deadline is approaching.',
      'I think we should prioritize this feature.',
      'Any questions?',
      "Let's schedule a follow-up meeting.",
      'Thanks everyone for joining.',
    ];

    // Generate a mock transcription by randomly selecting and repeating phrases
    let transcription = '';
    const paragraphCount = Math.floor(Math.random() * 5) + 3; // 3-7 paragraphs

    for (let i = 0; i < paragraphCount; i++) {
      let paragraph = '';
      const sentenceCount = Math.floor(Math.random() * 6) + 3; // 3-8 sentences per paragraph

      for (let j = 0; j < sentenceCount; j++) {
        const randomIndex = Math.floor(Math.random() * phrases.length);
        paragraph += phrases[randomIndex] + ' ';
      }

      transcription += paragraph.trim() + '\n\n';
    }

    return transcription.trim();
  }
}
