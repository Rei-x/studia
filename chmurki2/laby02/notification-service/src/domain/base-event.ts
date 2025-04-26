export abstract class BaseEvent {
  abstract serialize(): string;
  static deserialize(data: string): BaseEvent {
    throw new Error('Method deserialize must be implemented in child classes');
  }
}