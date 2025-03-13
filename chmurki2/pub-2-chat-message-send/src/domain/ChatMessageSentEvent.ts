import { BaseEvent } from './BaseEvent';

export class ChatMessageSentEvent extends BaseEvent {
  constructor(
    public meetingId: string,
    public message: string,
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      message: this.message,
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      message: string;
    };

    return new ChatMessageSentEvent(parsedData.meetingId, parsedData.message);
  }
}
