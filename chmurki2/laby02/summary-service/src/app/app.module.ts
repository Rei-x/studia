import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CqrsModule } from '@nestjs/cqrs';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { databaseConfig } from './config/database.config';

import { Summary } from 'src/domain/entities/summary.entity';
import { GenerateSummaryHandler } from './handlers/generate-summary.handler';
import { GetAllSummariesHandler } from './handlers/get-all-summaries.handler';
import { EventsController } from './controllers/events.controller';
import { SummaryGeneratedEvent } from 'src/domain/events/summary-generated.event';
import { SummariesModule } from 'src/web-api/summaries/summaries.module';

const CommandHandlers = [GenerateSummaryHandler];
const QueryHandlers = [GetAllSummariesHandler];
const Controllers = [EventsController];

@Module({
  imports: [
    ConfigModule.forRoot(),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) =>
        databaseConfig(configService.getOrThrow<string>('DATABASE_URL')),
    }),
    TypeOrmModule.forFeature([Summary]),
    ClientsModule.registerAsync([
      {
        imports: [ConfigModule],
        name: 'RABBIT_MQ_SERVICE',
        useFactory: (configService: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [configService.getOrThrow<string>('RABBIT_MQ_URL')],
            queue: SummaryGeneratedEvent.name,
            queueOptions: {
              durable: true,
            },
          },
        }),
        inject: [ConfigService],
      },
    ]),
    CqrsModule,
    SummariesModule,
  ],
  controllers: [...Controllers],
  providers: [...CommandHandlers, ...QueryHandlers],
})
export class AppModule {}
