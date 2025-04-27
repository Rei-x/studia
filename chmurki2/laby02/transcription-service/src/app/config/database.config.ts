import { TypeOrmModuleOptions } from '@nestjs/typeorm';

export const databaseConfig = (url: string): TypeOrmModuleOptions => ({
  type: 'postgres',
  url,
  entities: [__dirname + '/../../domain/**/*.entity{.ts,.js}'],
  synchronize: process.env.NODE_ENV !== 'production', // Auto-synchronize in development only
  logging: process.env.NODE_ENV !== 'production',
  ssl: {
    rejectUnauthorized: false, // Needed for some hosted PostgreSQL providers
  },
});
