import { Query } from '@nestjs/cqrs';
import type { Meeting } from 'src/domain/entities/meeting.entity';

export class GetMeetingsToStartQuery extends Query<Meeting[]> {
  constructor() {
    super();
  }
}
