import { BaseEvent } from './base-event';

export class MeetingStartedEvent extends BaseEvent {
  constructor(
    public meetingId: string,
    public title: string,
    public startTime: Date,
    public participantEmails?: string[],
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      title: this.title,
      startTime: this.startTime.toISOString(),
      participantEmails: this.participantEmails || [],
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      title: string;
      startTime: string;
      participantEmails: string[];
    };

    return new MeetingStartedEvent(
      parsedData.meetingId,
      parsedData.title,
      new Date(parsedData.startTime),
      parsedData.participantEmails,
    );
  }
}
