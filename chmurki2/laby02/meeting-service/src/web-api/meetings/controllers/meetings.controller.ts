import { Controller, Post, Body, Get } from '@nestjs/common';
import { CreateMeetingDto } from 'src/domain/dto/create-meeting.dto';
import { MeetingResponseDto } from 'src/domain/dto/meeting-response.dto';
import { MeetingApplicationService } from 'src/app/services/meeting-application.service';

@Controller('meetings')
export class MeetingsController {
  constructor(
    private readonly meetingApplicationService: MeetingApplicationService,
  ) {}

  @Post()
  async create(
    @Body() createMeetingDto: CreateMeetingDto,
  ): Promise<MeetingResponseDto> {
    return this.meetingApplicationService.create(createMeetingDto);
  }

  @Get()
  async findAll(): Promise<MeetingResponseDto[]> {
    return this.meetingApplicationService.findAll();
  }
}
