export function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());
}

export function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
}

export function camelize(obj: Record<string, any>): Record<string, any> {
  if (obj === null || obj === undefined || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => camelize(item));
  }

  const camelizedObj: Record<string, any> = {};

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const camelKey = toCamelCase(key);
      camelizedObj[camelKey] = camelize(obj[key]);
    }
  }

  return camelizedObj;
}

export function decamelize(obj: Record<string, any>): Record<string, any> {
  if (obj === null || obj === undefined || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => decamelize(item));
  }

  const snakeCasedObj: Record<string, any> = {};
  
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const snakeKey = toSnakeCase(key);
      snakeCasedObj[snakeKey] = decamelize((obj as Record<string, any>)[key]);
    }
  }
  
  return snakeCasedObj;
}
