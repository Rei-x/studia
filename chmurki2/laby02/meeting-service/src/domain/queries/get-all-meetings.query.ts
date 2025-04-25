import { Query } from '@nestjs/cqrs';
import type { Meeting } from 'src/domain/entities/meeting.entity';

export class GetAllMeetingsQuery extends Query<Meeting[]> {
  constructor() {
    super();
  }
}
