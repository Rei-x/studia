import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Meeting } from 'src/domain/entities/meeting.entity';
import { CreateMeetingDto } from 'src/domain/dto/create-meeting.dto';
import { MeetingResponseDto } from 'src/domain/dto/meeting-response.dto';
import { ClientProxy } from '@nestjs/microservices';
import { Inject } from '@nestjs/common';

@Injectable()
export class MeetingService {
  constructor(
    @InjectRepository(Meeting)
    private meetingRepository: Repository<Meeting>,
    @Inject('RABBIT_MQ_SERVICE') private readonly client: ClientProxy,
  ) {}

  async create(
    createMeetingDto: CreateMeetingDto,
  ): Promise<MeetingResponseDto> {
    const meeting = this.meetingRepository.create(createMeetingDto);

    const savedMeeting = await this.meetingRepository.save(meeting);
    return this.toResponseDto(savedMeeting);
  }

  async findAll(): Promise<MeetingResponseDto[]> {
    const meetings = await this.meetingRepository.find();
    return meetings.map((meeting) => this.toResponseDto(meeting));
  }

  private toResponseDto(meeting: Meeting): MeetingResponseDto {
    const responseDto = new MeetingResponseDto();
    Object.assign(responseDto, meeting);
    return responseDto;
  }
}
