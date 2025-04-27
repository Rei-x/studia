export class StartRecordingCommand {
  constructor(
    public readonly meetingId: string,
    public readonly title: string,
  ) {}
}
