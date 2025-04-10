export default {
  openapi: '3.1.0',
  info: {
    title: 'Library Management System API',
    description: 'API for managing books, authors, and lending operations',
    version: '1.0',
  },
  servers: [
    {
      url: 'https://java-webowka-znowu.sharkserver.kowalinski.dev',
      description: 'Production Server',
    },
    { url: 'http://localhost:8080', description: 'Local Development Server' },
  ],
  tags: [
    { name: 'Lending Management', description: 'APIs for managing book lending operations' },
    { name: 'Author Management', description: 'APIs for managing book authors' },
    { name: 'Book Management', description: 'APIs for managing books' },
  ],
  paths: {
    '/api/v1/books/{id}': {
      get: {
        tags: ['Book Management'],
        summary: 'Get book by ID',
        description: 'Retrieves a specific book by its ID',
        operationId: 'getBookById',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        responses: {
          '200': {
            description: 'Successfully retrieved the book',
            content: { '*/*': { schema: { $ref: '#/components/schemas/BookDTO' } } },
          },
          '404': { description: 'Book not found' },
          '500': { description: 'Internal server error' },
        },
      },
      put: {
        tags: ['Book Management'],
        summary: 'Update book',
        description: "Updates an existing book's information",
        operationId: 'updateBook',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        requestBody: {
          content: {
            'application/json': { schema: { $ref: '#/components/schemas/CreateBookDTO' } },
          },
          required: true,
        },
        responses: {
          '200': {
            description: 'Book successfully updated',
            content: { '*/*': { schema: { $ref: '#/components/schemas/BookDTO' } } },
          },
          '400': { description: 'Invalid input' },
          '404': { description: 'Book or Author not found' },
          '500': { description: 'Internal server error' },
        },
      },
      delete: {
        tags: ['Book Management'],
        summary: 'Delete book',
        description: 'Deletes a book from the system',
        operationId: 'deleteBook',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        responses: {
          '204': { description: 'Book successfully deleted' },
          '400': { description: 'Invalid input' },
          '404': { description: 'Book not found' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/authors/{id}': {
      get: {
        tags: ['Author Management'],
        summary: 'Get author by ID',
        description: 'Retrieves a specific author by their ID',
        operationId: 'getAuthorById',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        responses: {
          '200': {
            description: 'Successfully retrieved the author',
            content: { '*/*': { schema: { $ref: '#/components/schemas/AuthorDTO' } } },
          },
          '404': { description: 'Author not found' },
          '500': { description: 'Internal server error' },
        },
      },
      put: {
        tags: ['Author Management'],
        summary: 'Update author',
        description: "Updates an existing author's information",
        operationId: 'updateAuthor',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        requestBody: {
          content: {
            'application/json': { schema: { $ref: '#/components/schemas/CreateAuthorDTO' } },
          },
          required: true,
        },
        responses: {
          '200': {
            description: 'Author successfully updated',
            content: { '*/*': { schema: { $ref: '#/components/schemas/AuthorDTO' } } },
          },
          '400': { description: 'Invalid input' },
          '404': { description: 'Author not found' },
          '500': { description: 'Internal server error' },
        },
      },
      delete: {
        tags: ['Author Management'],
        summary: 'Delete author',
        description: 'Deletes an author from the system',
        operationId: 'deleteAuthor',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        responses: {
          '204': { description: 'Author successfully deleted' },
          '400': { description: 'Invalid input' },
          '404': { description: 'Author not found' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/lendings/return/{lendingId}': {
      post: {
        tags: ['Lending Management'],
        summary: 'Return a book',
        description: 'Marks a lending operation as returned',
        operationId: 'returnBook',
        parameters: [
          {
            name: 'lendingId',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        responses: {
          '200': {
            description: 'Book successfully returned',
            content: { '*/*': { schema: { $ref: '#/components/schemas/LendingDTO' } } },
          },
          '404': { description: 'Lending not found or already returned' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/lendings/lend': {
      post: {
        tags: ['Lending Management'],
        summary: 'Lend a book',
        description: 'Creates a new lending operation for a book',
        operationId: 'lendBook',
        requestBody: {
          content: {
            'application/json': { schema: { $ref: '#/components/schemas/CreateLendingDTO' } },
          },
          required: true,
        },
        responses: {
          '201': {
            description: 'Book successfully lent',
            content: { '*/*': { schema: { $ref: '#/components/schemas/LendingDTO' } } },
          },
          '400': { description: 'Invalid input' },
          '404': { description: 'Book not found or not available' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/books': {
      get: {
        tags: ['Book Management'],
        summary: 'Get all books',
        description: 'Retrieves a list of all books in the system',
        operationId: 'getAllBooks',
        responses: {
          '200': {
            description: 'Successfully retrieved all books',
            content: {
              '*/*': {
                schema: { type: 'array', items: { $ref: '#/components/schemas/BookDTO' } },
              },
            },
          },
          '500': { description: 'Internal server error' },
        },
      },
      post: {
        tags: ['Book Management'],
        summary: 'Create new book',
        description: 'Creates a new book in the system',
        operationId: 'createBook',
        requestBody: {
          content: {
            'application/json': { schema: { $ref: '#/components/schemas/CreateBookDTO' } },
          },
          required: true,
        },
        responses: {
          '201': {
            description: 'Book successfully created',
            content: { '*/*': { schema: { $ref: '#/components/schemas/BookDTO' } } },
          },
          '400': { description: 'Invalid input' },
          '404': { description: 'Author not found' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/authors': {
      get: {
        tags: ['Author Management'],
        summary: 'Get all authors',
        description: 'Retrieves a list of all authors in the system',
        operationId: 'getAllAuthors',
        responses: {
          '200': {
            description: 'Successfully retrieved all authors',
            content: {
              '*/*': {
                schema: { type: 'array', items: { $ref: '#/components/schemas/AuthorDTO' } },
              },
            },
          },
          '500': { description: 'Internal server error' },
        },
      },
      post: {
        tags: ['Author Management'],
        summary: 'Create new author',
        description: 'Creates a new author in the system',
        operationId: 'createAuthor',
        requestBody: {
          content: {
            'application/json': { schema: { $ref: '#/components/schemas/CreateAuthorDTO' } },
          },
          required: true,
        },
        responses: {
          '201': {
            description: 'Author successfully created',
            content: { '*/*': { schema: { $ref: '#/components/schemas/AuthorDTO' } } },
          },
          '400': { description: 'Invalid input' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/lendings': {
      get: {
        tags: ['Lending Management'],
        summary: 'Get all lendings',
        description: 'Retrieves a list of all lending operations',
        operationId: 'getAllLendings',
        responses: {
          '200': {
            description: 'Successfully retrieved all lendings',
            content: {
              '*/*': {
                schema: {
                  type: 'array',
                  items: { $ref: '#/components/schemas/LendingDTO' },
                },
              },
            },
          },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/lendings/{id}': {
      get: {
        tags: ['Lending Management'],
        summary: 'Get lending by ID',
        description: 'Retrieves a specific lending operation by its ID',
        operationId: 'getLendingById',
        parameters: [
          {
            name: 'id',
            in: 'path',
            required: true,
            schema: { type: 'integer', format: 'int32' },
          },
        ],
        responses: {
          '200': {
            description: 'Successfully retrieved the lending',
            content: { '*/*': { schema: { $ref: '#/components/schemas/LendingDTO' } } },
          },
          '404': { description: 'Lending not found' },
          '500': { description: 'Internal server error' },
        },
      },
    },
    '/api/v1/lendings/active': {
      get: {
        tags: ['Lending Management'],
        summary: 'Get active lendings',
        description: 'Retrieves a list of all active lending operations',
        operationId: 'getActiveLendings',
        responses: {
          '200': {
            description: 'Successfully retrieved active lendings',
            content: {
              '*/*': {
                schema: {
                  type: 'array',
                  items: { $ref: '#/components/schemas/LendingDTO' },
                },
              },
            },
          },
          '500': { description: 'Internal server error' },
        },
      },
    },
  },
  components: {
    schemas: {
      CreateBookDTO: {
        type: 'object',
        description: 'Data Transfer Object for creating a new book',
        properties: {
          title: { type: 'string', description: 'Title of the book', minLength: 1 },
          authorId: {
            type: 'integer',
            format: 'int32',
            description: "ID of the book's author",
            minimum: 1,
          },
          pages: {
            type: 'integer',
            format: 'int32',
            description: 'Number of pages in the book',
            minimum: 1,
          },
        },
        required: ['authorId', 'pages'],
      },
      AuthorDTO: {
        type: 'object',
        description: 'Data Transfer Object for Author responses',
        properties: {
          id: { type: 'integer', format: 'int32' },
          firstName: { type: 'string' },
          lastName: { type: 'string' },
          biography: { type: 'string' },
          fullName: { type: 'string' },
        },
      },
      BookDTO: {
        type: 'object',
        description: 'Data Transfer Object for Book responses',
        properties: {
          id: { type: 'integer', format: 'int32' },
          title: { type: 'string' },
          author: { $ref: '#/components/schemas/AuthorDTO' },
          pages: { type: 'integer', format: 'int32' },
          available: { type: 'boolean' },
        },
      },
      CreateAuthorDTO: {
        type: 'object',
        description: 'Data Transfer Object for creating a new author',
        properties: {
          firstName: {
            type: 'string',
            description: "Author's first name",
            maxLength: 50,
            minLength: 2,
          },
          lastName: {
            type: 'string',
            description: "Author's last name",
            maxLength: 50,
            minLength: 2,
          },
          biography: {
            type: 'string',
            description: "Author's biography",
            maxLength: 1000,
            minLength: 0,
          },
        },
      },
      LendingDTO: {
        type: 'object',
        description: 'Data Transfer Object for Lending responses',
        properties: {
          id: { type: 'integer', format: 'int32' },
          book: { $ref: '#/components/schemas/BookDTO' },
          readerName: { type: 'string' },
          lendDate: { type: 'string', format: 'date-time' },
          returnDate: { type: 'string', format: 'date-time' },
        },
      },
      CreateLendingDTO: {
        type: 'object',
        description: 'Data Transfer Object for creating a new lending',
        properties: {
          bookId: {
            type: 'integer',
            format: 'int32',
            description: 'ID of the book to be lent',
            minimum: 1,
          },
          readerName: {
            type: 'string',
            description: 'Name of the person borrowing the book',
            maxLength: 100,
            minLength: 2,
          },
        },
        required: ['bookId'],
      },
    },
  },
} as const
