import { Command } from '@nestjs/cqrs';

export class CreateMeetingCommand extends Command<string> {
  constructor(
    public readonly title: string,
    public readonly startTime: Date,
    public readonly description?: string,
    public readonly participants?: string[],
  ) {
    super();
  }
}
