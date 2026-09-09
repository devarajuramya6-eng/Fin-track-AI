export const CURRENCY_SYMBOLS: Record<string, string> = {
  USD: '$',
  INR: '₹',
  EUR: '€',
  GBP: '£',
  CAD: 'CA$',
};

export const getCurrencySymbol = (currency = 'USD'): string => {
  return CURRENCY_SYMBOLS[currency.toUpperCase()] || '$';
};

export const formatCurrency = (amount: number | string | undefined | null, currency = 'USD'): string => {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (num === undefined || num === null || isNaN(num)) {
    return `${getCurrencySymbol(currency)}0.00`;
  }

  const symbol = getCurrencySymbol(currency);
  
  // Format with localized decimals
  const formattedNumber = num.toLocaleString(currency === 'INR' ? 'en-IN' : 'en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  return `${symbol}${formattedNumber}`;
};
