export interface Document {
  page_content: string;
  metadata: Metadata;
  type: string;
}

export interface Metadata {
  filename: string;
  id: string;
  _id: string;
  _collection_name: string;
}

export interface Search {
  url:     string;
  content: string;
}

