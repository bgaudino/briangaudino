import {initChat} from '../ai_chat/js/chat.js';

document.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.elt === document.body) {
    // Re-initialize chat after browser back/forward navigation
    initChat();
  }
});
