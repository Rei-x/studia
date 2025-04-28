import { Injectable, Logger } from '@nestjs/common';
import { CommandBus, QueryBus } from '@nestjs/cqrs';
import { Cron } from '@nestjs/schedule';
import { DispatchMeetingStartedCommand } from '../../domain/commands/dispatch-meeting-started.command';
import { GetMeetingsToStartQuery } from '../../domain/queries/get-meetings-to-start.query';

@Injectable()
export class MeetingStarter {
  private readonly logger = new Logger(MeetingStarter.name);

  constructor(
    private readonly queryBus: QueryBus,
    private readonly commandBus: CommandBus,
  ) {}

  @Cron('*/5 * * * * *')
  async checkForStartingMeetings() {
    const startingMeetings = await this.queryBus.execute(
      new GetMeetingsToStartQuery(),
    );

    if (startingMeetings.length > 0) {
      this.logger.log(
        `Found ${startingMeetings.length} meetings to start: ${startingMeetings
          .map((meeting) => meeting.title)
          .join(', ')}`,
      );
    }

    for (const meeting of startingMeetings) {
      await this.commandBus.execute(
        new DispatchMeetingStartedCommand(meeting.id),
      );
    }
  }
}
