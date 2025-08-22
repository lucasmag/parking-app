// services/api.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_CONFIG } from '@/src/config/api';
import { camelize, decamelize, toSnakeCase } from './utils';

export type QueryParams = Record<string, string | number | boolean | null | undefined>;

class ApiClient {
  private baseURL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

  private async getAuthToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem('auth_token');
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    }
  }

  private buildUrl(endpoint: string, params?: QueryParams): string {
    const url = new URL(endpoint, this.baseURL)
    
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

    const response = await fetch(url, config)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return camelize(data) as TResponse;
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
