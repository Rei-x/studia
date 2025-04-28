import { CommandHandler, ICommandHandler, EventBus } from '@nestjs/cqrs';
import { DispatchMeetingStartedCommand } from '../../domain/commands/dispatch-meeting-started.command';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { Inject, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { MeetingStartedEvent } from 'src/domain/events/meeting-started.event';
import { firstValueFrom } from 'rxjs';

@CommandHandler(DispatchMeetingStartedCommand)
export class DispatchMeetingStartedHandler
  implements ICommandHandler<DispatchMeetingStartedCommand>
{
  private readonly logger = new Logger(DispatchMeetingStartedHandler.name);

  constructor(
    @InjectRepository(Meeting)
    private meetingRepository: Repository<Meeting>,
    @Inject('RECORDING_SERVICE') private readonly client: ClientProxy,
    private readonly eventBus: EventBus,
  ) {}

  async execute(command: DispatchMeetingStartedCommand): Promise<void> {
    const { meetingId } = command;

    const meeting = await this.meetingRepository.findOne({
      where: { id: meetingId },
    });

    if (!meeting) {
      this.logger.warn(`Meeting with ID ${meetingId} not found`);
      return;
    }

    if (meeting.startEventSent) {
      this.logger.log(
        `Meeting with ID ${meetingId} already has start event sent`,
      );
      return;
    }

    this.logger.log(`Meeting started: ${meeting.title} (ID: ${meeting.id})`);

    const event = new MeetingStartedEvent(
      meeting.id,
      meeting.title,
      meeting.startTime,
      meeting.participantEmails,
    );

    this.eventBus.publish(event);
    await firstValueFrom(
      this.client.emit(MeetingStartedEvent.name, event.serialize()),
    );

    meeting.startEventSent = true;
    await this.meetingRepository.save(meeting);
  }
}
