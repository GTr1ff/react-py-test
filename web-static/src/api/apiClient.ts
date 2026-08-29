import axios, {
  AxiosError,
  type AxiosInstance,
} from 'axios';
import { appConfig } from '../config/appConfig.ts';
import { ApiException } from '../exceptions/apiException.ts';
import { PaginatedResponse } from '../models/paginatedResponse.ts';

class ApiClient {
  private static _instance: ApiClient | null = null;
  private readonly _axios: AxiosInstance;

  private constructor() {
    this._axios = axios.create({
      baseURL: appConfig.apiBaseUrl,
      timeout: 30_000,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
    });

    if (appConfig.debugMode) {
      this._axios.interceptors.request.use((config) => {
        console.log(config.method?.toUpperCase(), config.url, config.data);
        return config;
      });
      this._axios.interceptors.response.use(
        (response) => {
          console.log(response.status, response.config.url, response.data);
          return response;
        },
        (error) => Promise.reject(error),
      );
    }

    this._axios.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => Promise.reject(this._handleError(error)),
    );
  }

  static get instance(): ApiClient {
    ApiClient._instance ??= new ApiClient();
    return ApiClient._instance;
  }

  async get<T>(
    path: string,
    options?: { params?: object; fromJson?: (data: unknown) => T },
  ): Promise<T> {
    const response = await this._axios.get(path, { params: options?.params });
    return options?.fromJson ? options.fromJson(response.data) : (response.data as T);
  }

  async getPaginated<T>(
    path: string,
    options: { params?: object; fromJson: (data: unknown) => T },
  ): Promise<PaginatedResponse<T>> {
    const response = await this._axios.get(path, { params: options.params });
    return PaginatedResponse.fromJson(response.data, options.fromJson);
  }

  async post<T>(
    path: string,
    options?: { data?: unknown; params?: object; fromJson?: (data: unknown) => T },
  ): Promise<T> {
    const response = await this._axios.post(path, options?.data, { params: options?.params });
    return options?.fromJson ? options.fromJson(response.data) : (response.data as T);
  }

  async put<T>(
    path: string,
    options?: { data?: unknown; params?: object; fromJson?: (data: unknown) => T },
  ): Promise<T> {
    const response = await this._axios.put(path, options?.data, { params: options?.params });
    return options?.fromJson ? options.fromJson(response.data) : (response.data as T);
  }

  async delete(path: string, options?: { params?: object }): Promise<void> {
    await this._axios.delete(path, { params: options?.params });
  }

  private _handleError(error: AxiosError): ApiException {
    if (error.response) {
      const { status, data } = error.response;
      let message = 'Unknown error occurred';
      if (data && typeof data === 'object') {
        const body = data as Record<string, unknown>;
        message = (body.detail as string) ?? (body.message as string) ?? message;
      } else if (typeof data === 'string') {
        message = data;
      }
      return new ApiException(message, status, data);
    }

    if (error.code === 'ECONNABORTED') {
      return new ApiException('Connection timeout');
    }
    if (error.code === 'ERR_NETWORK') {
      return new ApiException('No internet connection');
    }
    return new ApiException(error.message ?? 'Unknown error');
  }
}

export const apiClient = ApiClient.instance;
export { ApiClient };