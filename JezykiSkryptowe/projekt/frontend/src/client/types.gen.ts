// This file is auto-generated by @hey-api/openapi-ts

export type Body_upload_file_upload_post = {
    files: Array<((Blob | File))>;
};

export type FilePublic = {
    filename: string;
    on_disk: string;
    size: number;
    id: string;
    created_at: string;
};

export type HTTPValidationError = {
    detail?: Array<ValidationError>;
};

export type MessageKind = 'message' | 'tool_start' | 'tool_output';

export type MessagePublic = {
    content: string;
    sent_by?: SentBy;
    kind?: MessageKind;
    tool_name?: string | null;
    id: string;
    thread_id: string;
};

export type ResponseModel = {
    message: string;
};

export type SentBy = 'user' | 'bot';

export type ThreadPublicWithMessages = {
    title: string;
    created_at?: string;
    id: string;
    messages: Array<MessagePublic>;
};

export type ValidationError = {
    loc: Array<(string | number)>;
    msg: string;
    type: string;
};

export type RootGetResponse = ResponseModel;

export type MessagesMessagesGetResponse = Array<MessagePublic>;

export type FilesFilesGetResponse = Array<FilePublic>;

export type DeleteFileFilesFileIdDeleteData = {
    fileId: string;
};

export type DeleteFileFilesFileIdDeleteResponse = ResponseModel;

export type ThreadsThreadsGetResponse = Array<ThreadPublicWithMessages>;

export type UploadFileUploadPostData = {
    formData: Body_upload_file_upload_post;
};

export type UploadFileUploadPostResponse = unknown;

export type $OpenApiTs = {
    '/': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: ResponseModel;
            };
        };
    };
    '/messages': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: Array<MessagePublic>;
            };
        };
    };
    '/files': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: Array<FilePublic>;
            };
        };
    };
    '/files/{file_id}': {
        delete: {
            req: DeleteFileFilesFileIdDeleteData;
            res: {
                /**
                 * Successful Response
                 */
                200: ResponseModel;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/threads': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: Array<ThreadPublicWithMessages>;
            };
        };
    };
    '/upload': {
        post: {
            req: UploadFileUploadPostData;
            res: {
                /**
                 * Successful Response
                 */
                200: unknown;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
};