import { BaseEvent } from './BaseEvent';

export class MeetingStartedEvent extends BaseEvent {
  constructor(
    public meetingId: string,
    public startTime: string,
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      startTime: this.startTime,
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      startTime: string;
    };

    return new MeetingStartedEvent(parsedData.meetingId, parsedData.startTime);
  }
}
