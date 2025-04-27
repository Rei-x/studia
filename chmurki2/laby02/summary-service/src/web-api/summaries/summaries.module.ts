import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';
import { SummariesController } from './controllers/summaries.controller';

@Module({
  imports: [CqrsModule],
  controllers: [SummariesController],
  providers: [],
})
export class SummariesModule {}
