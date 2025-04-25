import { IQuery } from '@nestjs/cqrs';
import { Meeting } from 'src/domain/entities/meeting.entity';

export class GetAllMeetingsQuery implements IQuery {
  constructor() {}

  // Define the expected result type of this query
  readonly resultType!: Meeting[];
}
