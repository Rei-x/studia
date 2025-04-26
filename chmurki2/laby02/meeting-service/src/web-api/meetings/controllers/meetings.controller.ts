import { Controller, Post, Body, Get } from '@nestjs/common';
import { CommandBus, QueryBus } from '@nestjs/cqrs';
import { CreateMeetingDto } from 'src/domain/dto/create-meeting.dto';
import { CreateMeetingCommand } from 'src/domain/commands/create-meeting.command';
import { GetAllMeetingsQuery } from 'src/domain/queries/get-all-meetings.query';

@Controller('meetings')
export class MeetingsController {
  constructor(
    private readonly commandBus: CommandBus,
    private readonly queryBus: QueryBus,
  ) {}

  @Post()
  async create(@Body() createMeetingDto: CreateMeetingDto) {
    const { title, startTime, description, participants } = createMeetingDto;

    const command = new CreateMeetingCommand(
      title,
      new Date(startTime),
      description,
      participants,
    );

    const savedMeeting = await this.commandBus.execute(command);

    return savedMeeting;
  }

  @Get()
  async findAll() {
    const meetings = await this.queryBus.execute(new GetAllMeetingsQuery());
    return meetings;
  }
}
