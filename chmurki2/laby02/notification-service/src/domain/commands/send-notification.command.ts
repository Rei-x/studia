import { Command } from '@nestjs/cqrs';

export class SendNotificationCommand extends Command<void> {
  constructor(
    public readonly meetingId: string,
    public readonly title: string,
    public readonly startTime: Date,
    public readonly recipientEmails: string[],
    public readonly endTime?: Date,
  ) {
    super();
  }
}
