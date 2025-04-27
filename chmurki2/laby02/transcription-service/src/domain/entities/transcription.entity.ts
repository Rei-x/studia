import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('transcriptions')
export class Transcription {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  recordingId: string;

  @Column()
  meetingId: string;

  @Column()
  transcriptionUrl: string;

  @Column({ nullable: true, type: 'text' })
  content: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
