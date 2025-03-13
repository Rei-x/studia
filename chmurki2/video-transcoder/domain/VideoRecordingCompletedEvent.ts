import { BaseEvent } from "./BaseEvent";

export class VideoRecordingCompletedEvent extends BaseEvent {
  constructor(public recordingUrl: string) {
    super();
  }

  serialize() {
    return JSON.stringify({
      recordingUrl: this.recordingUrl,
    });
  }

  static deserialize(data: string) {
    const { recordingUrl } = JSON.parse(data);
    return new VideoRecordingCompletedEvent(recordingUrl);
  }
}
