import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('meetings')
export class Meeting {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ length: 255 })
  title: string;

  @Column('timestamp')
  startTime: Date;

  @Column({ nullable: true, type: 'timestamp' })
  endTime: Date;

  @Column('simple-array', { nullable: true })
  participantEmails: string[];

  @Column({ default: false })
  startEventSent: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
