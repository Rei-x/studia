export class CreateMeetingCommand {
  constructor(
    public readonly title: string,
    public readonly startTime: Date,
    public readonly participants?: string[],
  ) {}
}
