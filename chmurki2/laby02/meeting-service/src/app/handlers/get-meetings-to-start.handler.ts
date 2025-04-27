import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { GetMeetingsToStartQuery } from '../../domain/queries/get-meetings-to-start.query';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { Logger } from '@nestjs/common';

@QueryHandler(GetMeetingsToStartQuery)
export class GetMeetingsToStartHandler
  implements IQueryHandler<GetMeetingsToStartQuery>
{
  private readonly logger = new Logger(GetMeetingsToStartHandler.name);

  constructor(
    @InjectRepository(Meeting)
    private meetingRepository: Repository<Meeting>,
  ) {}

  async execute(): Promise<Meeting[]> {
    const now = new Date();

    this.logger.debug('Querying for meetings that need to be started');

    return this.meetingRepository
      .createQueryBuilder('meeting')
      .where('meeting.startTime <= :now', { now })
      .andWhere('meeting.startEventSent = :sent', { sent: false })
      .getMany();
  }
}
