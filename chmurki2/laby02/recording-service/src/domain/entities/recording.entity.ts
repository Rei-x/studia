import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('recordings')
export class Recording {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ length: 255 })
  meetingId: string;

  @Column({ length: 255 })
  recordingUrl: string;

  @Column()
  durationSeconds: number;

  @Column({ length: 255 })
  status: 'in_progress' | 'completed' | 'failed';

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
