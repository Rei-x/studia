import { BaseEvent } from '../base-event';

export class MeetingCreatedEvent extends BaseEvent {
  constructor(
    public meetingId: string,
    public title: string,
    public startTime: Date,
    public endTime?: Date,
    public participantEmails?: string[],
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      title: this.title,
      startTime: this.startTime.toISOString(),
      endTime: this.endTime ? this.endTime.toISOString() : null,
      participantEmails: this.participantEmails || [],
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      title: string;
      startTime: string;
      endTime: string | null;
      participantEmails: string[];
    };

    return new MeetingCreatedEvent(
      parsedData.meetingId,
      parsedData.title,
      new Date(parsedData.startTime),
      parsedData.endTime ? new Date(parsedData.endTime) : undefined,
      parsedData.participantEmails,
    );
  }
}
