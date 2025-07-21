/**
 * Type-safe builder pattern for complex configurations
 */
export class ApiRequestBuilder<T = unknown> {
  private config: {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE';
    url: string;
    headers: Record<string, string>;
    timeout: number;
    retries: number;
    body?: unknown;
  };

  constructor(url: string) {
    this.config = {
      method: 'GET',
      url,
      headers: {},
      timeout: 30000,
      retries: 3,
    };
  }

  method<M extends 'GET' | 'POST' | 'PUT' | 'DELETE'>(
    method: M
  ): ApiRequestBuilder<M extends 'GET' | 'DELETE' ? never : T> {
    this.config.method = method;
    return this as any;
  }

  body<B>(body: B): ApiRequestBuilder<B> {
    if (this.config.method === 'GET' || this.config.method === 'DELETE') {
      throw new Error('Cannot set body on GET/DELETE requests');
    }
    this.config.body = body;
    return this as any;
  }

  header(key: string, value: string): this {
    this.config.headers[key] = value;
    return this;
  }

  timeout(ms: number): this {
    this.config.timeout = ms;
    return this;
  }

  build() {
    return Object.freeze({ ...this.config });
  }
}

// Usage - type safe!
const getRequest = new ApiRequestBuilder('/users')
  .method('GET')
  // .body({}) // Compile error! Can't set body on GET
  .timeout(5000)
  .build();

const postRequest = new ApiRequestBuilder('/users')
  .method('POST')
  .body({ name: 'John' }) // OK for POST
  .header('Content-Type', 'application/json')
  .build();