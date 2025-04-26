import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CqrsModule } from '@nestjs/cqrs';
import { databaseConfig } from './config/database.config';
import { SendNotificationHandler } from './handlers/send-notification.handler';
import { Participant } from '../domain/entities/participant.entity';
import { EventsController } from 'src/app/controllers/events.controller';

const CommandHandlers = [SendNotificationHandler];

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) =>
        databaseConfig(configService.getOrThrow<string>('DATABASE_URL')),
    }),
    TypeOrmModule.forFeature([Participant]),
    CqrsModule,
  ],
  controllers: [EventsController],
  providers: [...CommandHandlers],
})
export class AppModule {}
