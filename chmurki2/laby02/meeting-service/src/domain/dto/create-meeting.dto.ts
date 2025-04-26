import { Type } from 'class-transformer';
import {
  IsString,
  IsNotEmpty,
  IsOptional,
  IsArray,
  IsEmail,
  IsDate,
} from 'class-validator';

export class CreateMeetingDto {
  @IsString()
  @IsNotEmpty({ message: 'Meeting title is required' })
  title: string;

  @IsString()
  @IsOptional()
  description?: string;

  @Type(() => Date)
  @IsDate()
  @IsNotEmpty({ message: 'Start time is required' })
  startTime: string;

  @IsArray()
  @IsOptional()
  @IsEmail(
    {},
    { each: true, message: 'Each participant must be a valid email address' },
  )
  participants?: string[];
}
