import React, { useState } from 'react';
import { Bot, Send, Sparkles, AlertCircle } from 'lucide-react';
import { aiApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency } from '../../utils/formatters';

interface Message {
  sender: 'user' | 'assistant';
  text: string;
  data?: any;
  suggestion?: string;
  disclaimer?: string;
}

export const AIAssistant: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';

  const PRESET_PROMPTS = [
    'How much did I spend this month?',
    'Where did I spend the most?',
    'How much can I save?',
    'What is my total loan EMI obligation?',
    `Can I afford a ${formatCurrency(450, currency)} purchase?`,
    'How can I reduce my expenses?',
  ];

  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: 'assistant',
      text: "Hello! I am your Local AI Financial Assistant. I analyze your spending, calculate affordability, and evaluate your financial risk in real time—all computed locally on your device without transmitting data to external AI clouds.",
      suggestion: "Try selecting one of the suggested financial questions below or type your own question.",
      disclaimer: "Educational estimate only. This platform does not provide regulated financial advice.",
    },
  ]);

  const handleSend = async (questionText?: string) => {
    const textToSend = questionText || query;
    if (!textToSend.trim() || isLoading) return;

    const userMsg: Message = { sender: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    if (!questionText) setQuery('');
    setIsLoading(true);

    try {
      const res = await aiApi.queryAssistant(textToSend);
      const assistantMsg: Message = {
        sender: 'assistant',
        text: res.data.answer,
        data: res.data.calculated_data,
        suggestion: res.data.action_suggestion,
        disclaimer: res.data.disclaimer,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: "I encountered an error analyzing the local financial database. Please verify your connection.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
          <Bot className="w-7 h-7 text-emerald-500 dark:text-emerald-400" />
          <span>Local AI Financial Copilot</span>
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400">Deterministic NLP and mathematical decision intelligence executing 100% locally.</p>
      </div>

      {/* Preset Query Bubbles */}
      <div className="flex flex-wrap gap-2">
        {PRESET_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/40 text-xs text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white rounded-full transition"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Container */}
      <Card className="h-[520px] flex flex-col p-0 overflow-hidden border-slate-200 dark:border-slate-800">
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 dark:text-emerald-400 flex items-center justify-center flex-shrink-0 mt-1">
                  <Sparkles className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-xl rounded-2xl p-4 text-xs leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-emerald-500 text-slate-950 font-medium ml-12 shadow-sm'
                    : 'bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 mr-12'
                }`}
              >
                <div className="whitespace-pre-line">{msg.text}</div>

                {msg.suggestion && (
                  <div className="mt-3 pt-2.5 border-t border-slate-200 dark:border-slate-800 text-emerald-600 dark:text-emerald-400 font-semibold">
                    Tip: {msg.suggestion}
                  </div>
                )}

                {msg.disclaimer && (
                  <div className="mt-2 text-[10px] text-slate-500 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3 flex-shrink-0" />
                    <span>{msg.disclaimer}</span>
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-300 dark:bg-slate-700 text-slate-800 dark:text-slate-200 flex items-center justify-center flex-shrink-0 mt-1 text-xs font-bold uppercase">
                  U
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 items-center text-xs text-slate-500 dark:text-slate-400">
              <div className="w-8 h-8 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 dark:text-emerald-400 flex items-center justify-center">
                <Sparkles className="w-4 h-4 animate-spin" />
              </div>
              <span className="italic">Analyzing financial database...</span>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 flex gap-2"
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything about your income, spending, debt, or affordability..."
            className="flex-1 bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
          <Button type="submit" variant="primary" size="sm" isLoading={isLoading}>
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </Card>
    </div>
  );
};
