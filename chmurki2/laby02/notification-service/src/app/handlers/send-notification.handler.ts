import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { Logger } from '@nestjs/common';
import { SendNotificationCommand } from '../../domain/commands/send-notification.command';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Participant } from '../../domain/entities/participant.entity';

@CommandHandler(SendNotificationCommand)
export class SendNotificationHandler
  implements ICommandHandler<SendNotificationCommand>
{
  private readonly logger = new Logger(SendNotificationHandler.name);

  constructor(
    @InjectRepository(Participant)
    private participantRepository: Repository<Participant>,
  ) {}

  async execute(command: SendNotificationCommand): Promise<void> {
    const { meetingId, title, startTime, recipientEmails, endTime } = command;

    this.logger.log(
      `Processing notifications for meeting ${meetingId}: ${title}`,
    );

    for (const email of recipientEmails) {
      let participant = await this.participantRepository.findOne({
        where: { email },
      });

      if (!participant) {
        participant = this.participantRepository.create({ email });
        await this.participantRepository.save(participant);
        this.logger.log(`Created new participant record for ${email}`);
      }

      if (participant.notificationsEnabled) {
        this.logger.log(
          `Sending notification to ${email} about meeting "${title}" ` +
            `starting at ${startTime.toLocaleString()}` +
            `${endTime ? ` and ending at ${endTime.toLocaleString()}` : ''}`,
        );
      } else {
        this.logger.log(
          `Skipping notification for ${email} (notifications disabled)`,
        );
      }
    }

    this.logger.log(`Completed sending notifications for meeting ${meetingId}`);
  }
}
