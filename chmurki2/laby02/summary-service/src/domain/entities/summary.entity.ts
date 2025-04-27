import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('summaries')
export class Summary {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  meetingId: string;

  @Column()
  transcriptionId: string;

  @Column()
  recordingId: string;

  @Column({ type: 'text' })
  content: string;

  @Column({ nullable: true })
  summaryUrl: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
