import {
  IsString,
  IsOptional,
  IsDateString,
  IsArray,
  IsEmail,
} from 'class-validator';

export class UpdateMeetingDto {
  @IsString()
  @IsOptional()
  title?: string;

  @IsDateString()
  @IsOptional()
  startTime?: Date;

  @IsDateString()
  @IsOptional()
  endTime?: Date;

  @IsArray()
  @IsOptional()
  @IsEmail(
    {},
    { each: true, message: 'Each participant must be a valid email address' },
  )
  participantEmails?: string[];
}
