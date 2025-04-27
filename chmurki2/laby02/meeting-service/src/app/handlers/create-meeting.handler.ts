import { CommandHandler, ICommandHandler, EventBus } from '@nestjs/cqrs';
import { CreateMeetingCommand } from '../../domain/commands/create-meeting.command';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { Inject, Logger } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { MeetingCreatedEvent } from 'src/domain/events/meeting-created.event';

@CommandHandler(CreateMeetingCommand)
export class CreateMeetingHandler
  implements ICommandHandler<CreateMeetingCommand>
{
  private readonly logger = new Logger(CreateMeetingHandler.name);
  constructor(
    @InjectRepository(Meeting)
    private meetingRepository: Repository<Meeting>,
    @Inject('RABBIT_MQ_SERVICE') private readonly client: ClientProxy,
    private readonly eventBus: EventBus,
  ) {}

  async execute(command: CreateMeetingCommand): Promise<string> {
    const { title, startTime, participants } = command;
    this.logger.log(`Creating meeting with title: ${title}`);
    const meeting = this.meetingRepository.create({
      title,
      startTime,
      participantEmails: participants,
    });

    const savedMeeting = await this.meetingRepository.save(meeting);

    const event = new MeetingCreatedEvent(
      savedMeeting.id,
      savedMeeting.title,
      savedMeeting.startTime,
      savedMeeting.endTime,
      savedMeeting.participantEmails,
    );

    this.eventBus.publish(event);
    this.client.emit(MeetingCreatedEvent.name, event.serialize());

    this.logger.log(`Meeting created with ID: ${savedMeeting.id}`);
    return savedMeeting.id;
  }
}
