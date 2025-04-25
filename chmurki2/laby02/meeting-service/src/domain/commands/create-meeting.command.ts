import { Command } from '@nestjs/cqrs';
import type { Meeting } from 'src/domain/entities/meeting.entity';

export class CreateMeetingCommand extends Command<Meeting> {
  constructor(
    public readonly title: string,
    public readonly startTime: Date,
    public readonly description?: string,
    public readonly participants?: string[],
  ) {
    super();
  }
}
