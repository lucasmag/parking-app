// services/api.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_CONFIG } from '@/src/config/api';
import { camelize, decamelize, toSnakeCase } from './utils';

export type QueryParams = Record<string, string | number | boolean | null | undefined>;

export interface FetchSuccess<T> {
  data: T;
  error: null;
}

export interface FetchError {
  data: {};
  error: {
    message: string;
    status?: number;
  };
}

export type FetchResult<T> = FetchSuccess<T> | FetchError;

class ApiClient {
  private async getAuthToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem('auth_token');
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    }
  }

  private async safeFetch<T>(
    url: string,
    config?: RequestInit
  ): Promise<FetchResult<T>> {
    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorText = await response.text();
        console.log(`HTTP ${response.status} | ${errorText}`);

        return {
          data: {},
          error: {
            message: errorText || response.statusText,
            status: response.status,
          },
        };
      }

      const data = (await response.json()) as T;
      return { data, error: null };
    } catch (err) {
      console.log(err);
      return {
        data: {},
        error: {
          message: err instanceof Error ? err.message : "Network error",
        },
      };
    }
  }

  private buildUrl(endpoint: string, params?: QueryParams): string {
    const url = new URL(endpoint, API_CONFIG.base_url)
    
    if (params) {
      const searchParams = new URLSearchParams()
      
      Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
          searchParams.append(toSnakeCase(key), String(value))
        }
      })
      
      url.search = searchParams.toString()
    }
    
    return url.toString()
  }

  private async request<TResponse>(
    endpoint: string,
    options: RequestInit & { params?: QueryParams } = {}
  ): Promise<TResponse> {
    const { params, ...requestOptions } = options
    const url = this.buildUrl(endpoint, params)
    const token = await this.getAuthToken();

    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };
    
    const config: RequestInit = {
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
      ...requestOptions,
    }

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(decamelize(config.body))
    }
    console.log(url)
    const response = await this.safeFetch<TResponse>(url, config);
  
    return camelize(response.data || {}) as TResponse;
  }

  get<T>(endpoint: string, params?: QueryParams): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET', params })
  }

  post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data,
    })
  }

  put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data,
    })
  }

  delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

export const apiClient = new ApiClient();
