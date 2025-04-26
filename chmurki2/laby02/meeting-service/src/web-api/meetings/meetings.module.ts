import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';
import { MeetingsController } from './controllers/meetings.controller';

@Module({
  imports: [CqrsModule],
  controllers: [MeetingsController],
  providers: [],
})
export class MeetingsModule {}
