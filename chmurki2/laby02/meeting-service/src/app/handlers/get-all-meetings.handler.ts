import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { GetAllMeetingsQuery } from '../../domain/queries/get-all-meetings.query';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';

@QueryHandler(GetAllMeetingsQuery)
export class GetAllMeetingsHandler
  implements IQueryHandler<GetAllMeetingsQuery>
{
  constructor(
    @InjectRepository(Meeting)
    private meetingRepository: Repository<Meeting>,
  ) {}

  async execute(): Promise<Meeting[]> {
    return this.meetingRepository.find();
  }
}
