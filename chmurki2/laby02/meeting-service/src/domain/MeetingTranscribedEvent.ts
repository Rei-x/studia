import { BaseEvent } from './BaseEvent';

export class MeetingTranscribedEvent extends BaseEvent {
  constructor(public meetingId: string) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
    };

    return new MeetingTranscribedEvent(parsedData.meetingId);
  }
}
