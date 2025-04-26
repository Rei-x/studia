import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CqrsModule } from '@nestjs/cqrs';
import { databaseConfig } from './config/database.config';
import { SendNotificationHandler } from './handlers/send-notification.handler';
import { Participant } from '../domain/entities/participant.entity';

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
  providers: [...CommandHandlers],
})
export class AppModule {}
