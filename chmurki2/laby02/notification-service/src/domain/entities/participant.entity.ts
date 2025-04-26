import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('participants')
export class Participant {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ length: 255 })
  email: string;

  @Column({ length: 255, nullable: true })
  name: string;

  @Column({ default: true })
  notificationsEnabled: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
