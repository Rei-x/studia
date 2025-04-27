import { Controller, Get } from '@nestjs/common';
import { QueryBus } from '@nestjs/cqrs';
import { GetAllSummariesQuery } from 'src/domain/queries/get-all-summaries.query';

@Controller('summaries')
export class SummariesController {
  constructor(private readonly queryBus: QueryBus) {}

  @Get()
  async findAll() {
    return this.queryBus.execute(new GetAllSummariesQuery());
  }
}
