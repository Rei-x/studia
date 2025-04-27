import { Query } from '@nestjs/cqrs';
import type { Summary } from 'src/domain/entities/summary.entity';

export class GetAllSummariesQuery extends Query<Summary[]> {
  constructor() {
    super();
  }
}
