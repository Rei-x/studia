import {
  IsString,
  IsNotEmpty,
  IsDate,
  IsOptional,
  IsBoolean,
  IsArray,
  IsUUID,
} from 'class-validator';
import { Type } from 'class-transformer';

export class MeetingResponseDto {
  @IsUUID()
  @IsNotEmpty()
  id: string;

  @IsString()
  @IsNotEmpty()
  title: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsDate()
  @Type(() => Date)
  startTime: Date;

  @IsDate()
  @IsOptional()
  @Type(() => Date)
  endTime?: Date;

  @IsBoolean()
  isRecorded: boolean;

  @IsString()
  @IsOptional()
  recordingUrl?: string;

  @IsBoolean()
  isTranscribed: boolean;

  @IsString()
  @IsOptional()
  transcription?: string;

  @IsBoolean()
  isSummarized: boolean;

  @IsString()
  @IsOptional()
  summary?: string;

  @IsArray()
  @IsOptional()
  participants?: string[];

  @IsBoolean()
  notificationsSent: boolean;

  @IsDate()
  @Type(() => Date)
  createdAt: Date;

  @IsDate()
  @Type(() => Date)
  updatedAt: Date;
}
