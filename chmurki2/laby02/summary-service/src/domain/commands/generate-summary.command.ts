import { Command } from '@nestjs/cqrs';

export class GenerateSummaryCommand extends Command<string> {
  constructor(
    public readonly meetingId: string,
    public readonly recordingId: string,
    public readonly transcriptionUrl: string,
    public readonly transcriptionContent?: string,
  ) {
    super();
  }
}
