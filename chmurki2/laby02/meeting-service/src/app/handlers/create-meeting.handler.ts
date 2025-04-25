import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { CreateMeetingCommand } from '../../domain/commands/create-meeting.command';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { Inject } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';

@CommandHandler(CreateMeetingCommand)
export class CreateMeetingHandler
  implements ICommandHandler<CreateMeetingCommand>
{
  constructor(
    @InjectRepository(Meeting)
    private meetingRepository: Repository<Meeting>,
    @Inject('RABBIT_MQ_SERVICE') private readonly client: ClientProxy,
  ) {}

  async execute(command: CreateMeetingCommand): Promise<Meeting> {
    const { title, startTime, participants } = command;

    const meeting = this.meetingRepository.create({
      title,
      startTime,
      participantEmails: participants,
    });

    return this.meetingRepository.save(meeting);
  }
}
