import { RefreshCw, Share2, ArrowUp } from 'lucide-react';
import { useState, useRef } from 'react';

const ChatDetails = () => {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    // Handle submit logic here
    setInputValue('');
  };

  return (
    <div className="flex-1 bg-white flex flex-col h-full">
      {/* Chat message container */}
      <div className="flex-1 flex flex-col p-4 max-w-4xl mx-auto w-full overflow-y-auto pt-20">
        {/* User Question */}
        <div className="w-full mb-4 flex justify-end">
          <div className="bg-gray-100 text-black rounded-2xl px-6 py-3 max-w-[80%]">
            <p>what is time</p>
          </div>
        </div>
        
        {/* Assistant Answer */}
        <div className="w-full space-y-4 mb-4">
          <div className="flex items-start gap-4">
            <div className="flex-1rounded-2xl px-6 py-4">
              <div className="prose">
                <p>
                  Time is a fascinating and complex concept! At its most basic level, time is a measure of the progression of events, a way to sequence and compare the duration of things happening in the universe. It's often described as a dimension, much like space, where events have a past, present, and future.
                </p>
                <p>
                  From a scientific perspective, time is deeply tied to the fabric of the universe. In Einstein's theory of relativity, time isn't absolute—it can stretch or contract depending on speed and gravity. For example, time moves slightly slower near massive objects like Earth compared to in deep space. This isn't just theory; it's been proven with precise clocks!
                </p>
                <p>
                  Philosophically, time gets even trickier. Is it linear, flowing in one direction, or could it loop? Some thinkers, like Augustine, argued time is subjective, existing only in our minds as we perceive change. Others see it as an eternal "now" that we slice into moments.
                </p>
                <p>
                  Practically speaking, today is March 20, 2025, and time keeps ticking forward—at least as we experience it. What angle of time are you curious about? The physics, the philosophy, or something else?
                </p>
                
                {/* Interaction buttons */}
                <div className="flex space-x-4 pt-2">
                  <button className="p-2 hover:bg-gray-200 rounded-full cursor-pointer">
                    <RefreshCw className="w-4 h-4 text-gray-600" />
                  </button>
                  <button className="p-2 hover:bg-gray-200 rounded-full cursor-pointer">
                    <Share2 className="w-4 h-4 text-gray-600" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Chat input */}
      <div className="p-4">
        <div className="max-w-4xl mx-auto w-full">
          <form onSubmit={handleSubmit} className="relative bg-white rounded-2xl shadow-sm border border-gray-200">
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              placeholder="What would you like to know?"
              rows={1}
              className="w-full min-h-[100px] max-h-[800px] py-4 px-4 pr-12 rounded-2xl focus:outline-none resize-none overflow-y-hidden"
            />
            <button 
              type="submit" 
              className="absolute right-2 bottom-2 bg-gray-200 rounded-full p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-300 cursor-pointer disabled:opacity-40"
              disabled={!inputValue.trim()}
            >
              <ArrowUp className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatDetails;
