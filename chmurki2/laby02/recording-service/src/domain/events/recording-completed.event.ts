import { BaseEvent } from '../base-event';

export class RecordingCompletedEvent extends BaseEvent {
  constructor(
    public recordingId: string,
    public meetingId: string,
    public recordingUrl: string,
    public durationSeconds: number,
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      recordingId: this.recordingId,
      meetingId: this.meetingId,
      recordingUrl: this.recordingUrl,
      durationSeconds: this.durationSeconds,
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      recordingId: string;
      meetingId: string;
      recordingUrl: string;
      durationSeconds: number;
    };

    return new RecordingCompletedEvent(
      parsedData.recordingId,
      parsedData.meetingId,
      parsedData.recordingUrl,
      parsedData.durationSeconds,
    );
  }
}
