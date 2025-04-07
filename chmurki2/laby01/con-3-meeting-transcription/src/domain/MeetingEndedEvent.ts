import { BaseEvent } from './BaseEvent';

export class MeetingEndedEvent extends BaseEvent {
  constructor(
    public meetingId: string,
    public endTime: Date,
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      endTime: this.endTime.toISOString(),
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      endTime: string;
    };

    return new MeetingEndedEvent(
      parsedData.meetingId,
      new Date(parsedData.endTime),
    );
  }
}
