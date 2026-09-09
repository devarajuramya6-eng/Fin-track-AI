import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className,
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary: 'bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold focus:ring-emerald-500 shadow-sm shadow-emerald-500/20',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-100 focus:ring-slate-600 border border-slate-700',
    danger: 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 focus:ring-rose-500',
    ghost: 'hover:bg-slate-800 text-slate-300 hover:text-white',
    outline: 'border border-slate-700 hover:border-slate-600 text-slate-300 hover:text-white',
  };

  const sizes = {
    sm: 'px-2.5 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  return (
    <button
      className={twMerge(clsx(baseStyles, variants[variant], sizes[size], className))}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <span className="w-4 h-4 mr-2 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
      )}
      {children}
    </button>
  );
};
