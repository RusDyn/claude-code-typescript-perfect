/**
 * Result pattern for explicit error handling
 * This eliminates try-catch blocks and makes errors part of the type system
 */
export type Result<T, E = Error> =
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };

// Constructors
export const Ok = <T>(data: T): Result<T, never> => ({
  success: true,
  data,
});

export const Err = <E>(error: E): Result<never, E> => ({
  success: false,
  error,
});

// Type guards
export const isOk = <T, E>(
  result: Result<T, E>
): result is { success: true; data: T } => result.success;

export const isErr = <T, E>(
  result: Result<T, E>
): result is { success: false; error: E } => !result.success;

// Combinators
export const map = <T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> => (isOk(result) ? Ok(fn(result.data)) : result);

export const flatMap = <T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> => (isOk(result) ? fn(result.data) : result);

export const mapError = <T, E, F>(
  result: Result<T, E>,
  fn: (error: E) => F
): Result<T, F> => (isErr(result) ? Err(fn(result.error)) : result);

// Utility functions
export const collect = <T, E>(
  results: Result<T, E>[]
): Result<T[], E> => {
  const values: T[] = [];
  for (const result of results) {
    if (isErr(result)) return result;
    values.push(result.data);
  }
  return Ok(values);
};