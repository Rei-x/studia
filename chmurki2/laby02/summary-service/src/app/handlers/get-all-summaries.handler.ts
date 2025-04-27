import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { GetAllSummariesQuery } from '../../domain/queries/get-all-summaries.query';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Summary } from 'src/domain/entities/summary.entity';

@QueryHandler(GetAllSummariesQuery)
export class GetAllSummariesHandler
  implements IQueryHandler<GetAllSummariesQuery>
{
  constructor(
    @InjectRepository(Summary)
    private summaryRepository: Repository<Summary>,
  ) {}

  async execute(): Promise<Summary[]> {
    return this.summaryRepository.find();
  }
}
