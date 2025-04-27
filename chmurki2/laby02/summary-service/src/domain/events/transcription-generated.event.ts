import { BaseEvent } from '../base-event';

export class TranscriptionGeneratedEvent extends BaseEvent {
  constructor(
    public readonly meetingId: string,
    public readonly recordingId: string,
    public readonly transcriptionUrl: string,
    public readonly durationSeconds: number,
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      recordingId: this.recordingId,
      transcriptionUrl: this.transcriptionUrl,
      durationSeconds: this.durationSeconds,
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      recordingId: string;
      transcriptionUrl: string;
      durationSeconds: number;
    };

    return new TranscriptionGeneratedEvent(
      parsedData.meetingId,
      parsedData.recordingId,
      parsedData.transcriptionUrl,
      parsedData.durationSeconds,
    );
  }
}
