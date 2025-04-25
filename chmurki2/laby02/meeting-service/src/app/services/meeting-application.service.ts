import { Injectable } from '@nestjs/common';
import { CommandBus, QueryBus } from '@nestjs/cqrs';
import { CreateMeetingCommand } from '../../domain/commands/create-meeting.command';
import { GetAllMeetingsQuery } from '../../domain/queries/get-all-meetings.query';
import { CreateMeetingDto } from 'src/domain/dto/create-meeting.dto';
import { MeetingResponseDto } from 'src/domain/dto/meeting-response.dto';
import { Meeting } from 'src/domain/entities/meeting.entity';

@Injectable()
export class MeetingApplicationService {
  constructor(
    private readonly commandBus: CommandBus,
    private readonly queryBus: QueryBus,
  ) {}

  async create(
    createMeetingDto: CreateMeetingDto,
  ): Promise<MeetingResponseDto> {
    const { title, description, startTime, participants } = createMeetingDto;

    const command = new CreateMeetingCommand(
      title,
      startTime,
      description,
      participants,
    );

    const meeting = await this.commandBus.execute(command);
    return this.toResponseDto(meeting);
  }

  async findAll(): Promise<MeetingResponseDto[]> {
    const query = new GetAllMeetingsQuery();
    const meetings = await this.queryBus.execute(query);
    return meetings.map((meeting) => this.toResponseDto(meeting));
  }

  private toResponseDto(meeting: Meeting): MeetingResponseDto {
    const responseDto = new MeetingResponseDto();
    Object.assign(responseDto, meeting);
    return responseDto;
  }
}
