import { BaseEvent } from '../base-event';

export class SummaryGeneratedEvent extends BaseEvent {
  constructor(
    public readonly meetingId: string,
    public readonly summaryId: string,
    public readonly summaryUrl: string,
  ) {
    super();
  }

  serialize() {
    return JSON.stringify({
      meetingId: this.meetingId,
      summaryId: this.summaryId,
      summaryUrl: this.summaryUrl,
    });
  }

  static deserialize(data: string) {
    const parsedData = JSON.parse(data) as {
      meetingId: string;
      summaryId: string;
      summaryUrl: string;
    };

    return new SummaryGeneratedEvent(
      parsedData.meetingId,
      parsedData.summaryId,
      parsedData.summaryUrl,
    );
  }
}
