export type CmsRecord = Record<string, unknown> & {
  uuid?: string;
  id?: string | number;
  title?: string;
  name?: string;
  is_active?: boolean;
  status?: string;
};

export type PageResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
};

export type ToastTone = "success" | "error" | "info";
