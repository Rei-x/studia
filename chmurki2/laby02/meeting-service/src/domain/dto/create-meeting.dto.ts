import {
  IsString,
  IsNotEmpty,
  IsDateString,
  IsOptional,
  IsArray,
  IsEmail,
} from 'class-validator';

export class CreateMeetingDto {
  @IsString()
  @IsNotEmpty({ message: 'Meeting title is required' })
  title: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsDateString()
  @IsNotEmpty({ message: 'Start time is required' })
  startTime: Date;

  @IsArray()
  @IsOptional()
  @IsEmail(
    {},
    { each: true, message: 'Each participant must be a valid email address' },
  )
  participants?: string[];
}
