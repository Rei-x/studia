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
    // Use query bus to get meetings that need to start
    const startingMeetings = await this.queryBus.execute(
      new GetMeetingsToStartQuery(),
    );

    this.logger.debug(`Found ${startingMeetings.length} meetings starting now`);

    // Use command bus to dispatch start events
    for (const meeting of startingMeetings) {
      await this.commandBus.execute(
        new DispatchMeetingStartedCommand(meeting.id),
      );
    }
  }
}
