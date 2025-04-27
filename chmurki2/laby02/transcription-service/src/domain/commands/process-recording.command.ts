import { Command } from '@nestjs/cqrs';

export class ProcessRecordingCommand extends Command<string> {
  constructor(
    public readonly recordingId: string,
    public readonly meetingId: string,
    public readonly recordingUrl: string,
    public readonly durationSeconds: number,
  ) {
    super();
  }
}
