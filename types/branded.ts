declare const __brand: unique symbol;
type Brand<B> = { [__brand]: B };
export type Branded<T, B> = T & Brand<B>;

// Domain types that can't be confused
export type UserId = Branded<string, 'UserId'>;
export type Email = Branded<string, 'Email'>;
export type NonEmptyString = Branded<string, 'NonEmptyString'>;
export type PositiveInteger = Branded<number, 'PositiveInteger'>;

// Smart constructors with validation
export const UserId = {
  create(value: string): Result<UserId, string> {
    if (!value.startsWith('user_')) {
      return Err('User ID must start with "user_"');
    }
    if (value.length !== 25) {
      return Err('User ID must be 25 characters');
    }
    return Ok(value as UserId);
  },
  
  unsafeCreate(value: string): UserId {
    return value as UserId;
  },
};

export const Email = {
  create(value: string): Result<Email, string> {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      return Err('Invalid email format');
    }
    return Ok(value.toLowerCase() as Email);
  },
};

// Usage example showing type safety
function sendEmail(to: Email, subject: NonEmptyString): Result<void, Error> {
  // Can't accidentally pass UserId here - compile error!
  // Implementation...
  return Ok(undefined);
}