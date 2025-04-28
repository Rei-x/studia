import { CommandHandler, ICommandHandler, EventBus } from '@nestjs/cqrs';
import { GenerateSummaryCommand } from '../../domain/commands/generate-summary.command';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Summary } from 'src/domain/entities/summary.entity';
import { Inject, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { SummaryGeneratedEvent } from 'src/domain/events/summary-generated.event';
import { firstValueFrom } from 'rxjs';

@CommandHandler(GenerateSummaryCommand)
export class GenerateSummaryHandler
  implements ICommandHandler<GenerateSummaryCommand>
{
  private readonly logger = new Logger(GenerateSummaryHandler.name);

  constructor(
    @InjectRepository(Summary)
    private summaryRepository: Repository<Summary>,
    @Inject('RABBIT_MQ_SERVICE') private readonly client: ClientProxy,
    private readonly eventBus: EventBus,
  ) {}

  async execute(command: GenerateSummaryCommand): Promise<string> {
    const { meetingId, recordingId, transcriptionUrl, transcriptionContent } =
      command;

    this.logger.log(`Fetching transcription from ${transcriptionUrl}...`);
    await this.delay(800);

    this.logger.log('Generating AI summary...');
    await this.delay(1500);
    const summaryContent = this.generateMockSummary(transcriptionContent);
    this.logger.log('Summary generated successfully');

    this.logger.log('Uploading summary to storage...');
    await this.delay(500);
    const summaryUrl = `https://example-storage.com/summaries/${meetingId}.txt`;
    this.logger.log(`Summary uploaded to ${summaryUrl}`);

    const summary = this.summaryRepository.create({
      meetingId,
      recordingId,
      transcriptionId: recordingId,
      content: summaryContent,
      summaryUrl,
    });

    const savedSummary = await this.summaryRepository.save(summary);

    const event = new SummaryGeneratedEvent(
      meetingId,
      savedSummary.id,
      summaryUrl,
    );

    this.eventBus.publish(event);
    await firstValueFrom(
      this.client.emit(SummaryGeneratedEvent.name, event.serialize()),
    );

    this.logger.log(`Summary completed for meeting ID: ${meetingId}`);

    return savedSummary.id;
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private generateMockSummary(transcriptionContent?: string): string {
    if (transcriptionContent) {
      const paragraphs = transcriptionContent.split('\n\n');
      if (paragraphs.length > 0) {
        return `Summary: ${paragraphs[0].substring(0, 100)}... [AI generated summary: The meeting discussed key project milestones and action items. Participants agreed on next steps and assigned responsibilities. The team will follow up in the next meeting scheduled for next week.]`;
      }
    }

    const summaryTemplates = [
      'The meeting focused on project updates and upcoming deadlines. Team members reported progress on their assigned tasks.',
      'The team discussed the latest product features and customer feedback. Several action items were identified for follow-up.',
      "A strategy session where the team planned the next quarter's objectives. Key performance indicators were reviewed.",
      'This meeting addressed recent challenges in the development process. Solutions were proposed and assigned to team members.',
      'A collaborative session where team members brainstormed new ideas for improving the product. Several promising concepts were selected for further exploration.',
    ];

    const actionItems = [
      'Action items: Update documentation by Friday.',
      'Action items: Schedule follow-up meetings with stakeholders.',
      "Action items: Revise the project timeline based on today's discussion.",
      'Action items: Distribute meeting notes to all participants.',
      'Action items: Prepare product demo for next meeting.',
    ];

    const randomSummary =
      summaryTemplates[Math.floor(Math.random() * summaryTemplates.length)];
    const randomActionItem =
      actionItems[Math.floor(Math.random() * actionItems.length)];

    return `${randomSummary}\n\n${randomActionItem}`;
  }
}
