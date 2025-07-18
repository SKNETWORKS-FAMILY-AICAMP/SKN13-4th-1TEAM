document.addEventListener('DOMContentLoaded', function() {
    const chatSearchForm = document.getElementById('chatSearchForm');
    const chatSearchInput = document.getElementById('chatSearchInput');
    const toggleSearchDiv = document.getElementById('toggleSearch');

    if (toggleSearchDiv) {
        toggleSearchDiv.addEventListener('click', () => {
            chatSearchForm.classList.toggle('visible');
        });
    }

    chatSearchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const query = chatSearchInput.value.trim();

        try {
            const response = await fetch(`/api/chat/search/?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            const sessionIds = data.session_ids;

            const allSessionItems = document.querySelectorAll('.chat-session-item');
            allSessionItems.forEach(item => {
                const sessionId = item.dataset.sessionId;
                if (sessionIds.includes(parseInt(sessionId, 10))) {
                    item.style.display = ''; // 보이게
                } else {
                    item.style.display = 'none'; // 숨김
                }
            });
        } catch (error) {
            console.error('Error searching chats:', error);
        }
    });

    const sidebarToggle = document.getElementById('sidebarToggle');
    const chatSidebar = document.querySelector('.chat-sidebar');
    const chatWrapper = document.querySelector('.chat-wrapper');
    const toggleHistory = document.getElementById('toggle-history');
    const sessionList = document.querySelector('.sidebar-session-list');

    const textSpans = document.querySelectorAll('.sidebar-item > span:not(.material-symbols-outlined)');

    sidebarToggle.addEventListener('click', () => {
        const isSidebarAboutToCollapse = !chatSidebar.classList.contains('collapsed');

        if (isSidebarAboutToCollapse) {
            // --- COLLAPSING THE SIDEBAR ---
            // 1. Hide text instantly
            textSpans.forEach(span => span.classList.add('hide-text'));

            // 2. Collapse history list instantly
            const isHistoryOpen = sessionList.style.maxHeight !== '0px';
            sessionStorage.setItem('chatHistoryWasOpen', isHistoryOpen.toString());

            if (isHistoryOpen) {
                sessionList.style.transition = 'none'; // Disable transition
                sessionList.style.maxHeight = '0px';
                sessionStorage.setItem('chatHistoryOpen', 'false');

                requestAnimationFrame(() => {
                    sessionList.style.transition = 'max-height 0.2s ease-in-out'; // Restore transition
                });
            }

            // 3. Then collapse the sidebar
            chatSidebar.classList.add('collapsed');
            chatWrapper.classList.add('sidebar-collapsed');
            toggleIcon.textContent = 'chevron_right'; // 아이콘 변경

        } else {
            // --- EXPANDING THE SIDEBAR ---
            // 1. Expand the sidebar first
            chatSidebar.classList.remove('collapsed');
            chatWrapper.classList.remove('sidebar-collapsed');

            // 2. Listen for the end of the sidebar's transition
            const onSidebarTransitionEnd = () => {
                chatSidebar.removeEventListener('transitionend', onSidebarTransitionEnd);

                // 3. Show text
                textSpans.forEach(span => span.classList.remove('hide-text'));

                // 4. Expand history list after sidebar is expanded
                const wasHistoryOpen = sessionStorage.getItem('chatHistoryWasOpen') === 'true';
                if (wasHistoryOpen) {
                    sessionList.classList.remove('collapsed'); // Remove collapsed class
                    sessionList.style.maxHeight = sessionList.scrollHeight + 'px'; // Animate to scrollHeight
                    sessionStorage.setItem('chatHistoryOpen', 'true');
                }
            };
            chatSidebar.addEventListener('transitionend', onSidebarTransitionEnd);
        }
    });

    if (toggleHistory && sessionList) {
        // Initial state: check sessionStorage for previous state, default to open
        const isHistoryOpen = sessionStorage.getItem('chatHistoryOpen') === 'true';

        sessionStorage.setItem('chatHistoryOpen', isHistoryOpen.toString()); // Store initial state

        toggleHistory.addEventListener('click', () => {
            const isCurrentlyCollapsed = sessionList.classList.contains('collapsed');
            if (isCurrentlyCollapsed) {
                // Expand the list
                sessionList.classList.remove('collapsed');
                sessionList.style.maxHeight = sessionList.scrollHeight + 'px'; // Animate to scrollHeight
                sessionStorage.setItem('chatHistoryOpen', 'true');
            } else {
                // Collapse the list
                sessionList.classList.add('collapsed');
                sessionList.style.maxHeight = '0px'; // Animate to 0
                sessionStorage.setItem('chatHistoryOpen', 'false');
            }
        });
    }

    // ✅ 페이지 전체를 아래로 자동 스크롤
    scrollToBottom();

    // --- Delete Session Logic (using event delegation) ---
    const chatSessionListContainer = document.querySelector('.sidebar-session-list'); // The parent container for session items

    if (chatSessionListContainer) {
        chatSessionListContainer.addEventListener('click', (event) => {
            const button = event.target.closest('.delete-session-btn'); // Find the clicked delete button

            if (!button) return; // If click was not on a delete button, do nothing

            event.preventDefault(); // Prevent default link behavior (if any)
            event.stopPropagation(); // Prevent chat-session-item click event

            const sessionItem = button.closest('.chat-session-item');
            const sessionId = sessionItem.dataset.sessionId;

            // Create confirmation dialog
            const dialogOverlay = document.createElement('div');
            dialogOverlay.classList.add('confirmation-dialog-overlay');

            const dialog = document.createElement('div');
            dialog.classList.add('confirmation-dialog');
            dialog.innerHTML = `
                <p>그 세션을 지우시겠습니까?</p>
                <div class="confirmation-dialog-buttons">
                    <button class="confirm-yes">YES</button>
                    <button class="confirm-no">NO</button>
                </div>
            `;

            dialogOverlay.appendChild(dialog);
            document.body.appendChild(dialogOverlay); // Append to body to be on top

            // Position the dialog relative to the sidebar
            const sidebarRect = chatSidebar.getBoundingClientRect();
            dialog.style.position = 'fixed'; // Use fixed for viewport relative positioning
            dialog.style.top = `${sidebarRect.top + 20}px`; // A bit from the top of sidebar
            dialog.style.left = `${sidebarRect.right + 20}px`; // To the right of sidebar
            dialog.style.transform = 'translateX(0)'; // Reset transform if any
            dialog.style.maxWidth = '250px'; // Limit width
            dialog.style.width = 'auto'; // Adjust width based on content


            // Add event listeners to dialog buttons
            dialog.querySelector('.confirm-yes').addEventListener('click', async () => {
                // Perform deletion
                try {
                    const response = await fetch(`/api/chat/session/${sessionId}/delete/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    });

                    if (response.ok) {
                        // Remove from DOM
                        sessionItem.remove();
                        // If the deleted session was the active one, redirect to a new chat
                        if (sessionItem.classList.contains('active')) {
                            window.location.href = '/chatbot/'; // Redirect to the view that handles latest/new session
                        }
                    } else {
                        console.error('Failed to delete session:', response.statusText);
                        alert('세션 삭제에 실패했습니다.');
                    }
                } catch (error) {
                    console.error('Error deleting session:', error);
                    alert('세션 삭제 중 오류가 발생했습니다.');
                } finally {
                    dialogOverlay.remove(); // Remove dialog
                }
            });

            dialog.querySelector('.confirm-no').addEventListener('click', () => {
                dialogOverlay.remove(); // Remove dialog
            });
        });
    }
});

console.log('chatbot.js loaded successfully!');

const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMain = document.querySelector('.chat-main');

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const msg = userInput.value.trim();
  if (!msg) return;

  appendMessage('user', msg);
  userInput.value = '';

  const pathParts = window.location.pathname.split('/').filter(Boolean);
  const lastPart = pathParts.pop();
  const sessionId = /^[0-9]+$/.test(lastPart) ? lastPart : null;

  try {
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ 
        message: msg,
        session_id: sessionId
      }),
    });

    const data = await response.json();
    appendMessage('assistant', data.reply);

    if (data.new_session_id) {
      const newSessionId = data.new_session_id;
      const newUrl = `/chatbot/${newSessionId}/`;
      history.pushState({path: newUrl}, '', newUrl);

      const newSessionItem = document.createElement('a');
      newSessionItem.href = newUrl;
      newSessionItem.classList.add('chat-session-item', 'active');
      newSessionItem.dataset.sessionId = newSessionId;
      newSessionItem.innerHTML = `
        <span class="material-symbols-outlined">chat</span>
        <span class="session-title">대화 시작...</span>
        <span class="material-symbols-outlined delete-session-btn">close</span>
      `;

      const existingActive = document.querySelector('.chat-session-item.active');
      if (existingActive) {
        existingActive.classList.remove('active');
      }

      const sessionList = document.querySelector('ul.chat-session-list');
      const emptyMessage = document.querySelector('.chat-session-empty');
      if (emptyMessage) {
        emptyMessage.remove();
      }
      sessionList.prepend(newSessionItem);

      // 제목 업데이트 요청
      updateTitle(newSessionId, msg);
    }

  } catch (error) {
    console.error('Error sending message:', error);
    appendMessage('assistant', '메시지를 보내는 중 오류가 발생했습니다.');
  }
});

async function updateTitle(sessionId, firstMessage) {
  try {
    const response = await fetch(`/api/chat/update_title/${sessionId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ first_message: firstMessage }),
    });
    const data = await response.json();
    if (data.status === 'success') {
      // DOM에서 세션 아이템을 다시 찾아 제목을 업데이트합니다.
      const sessionItemToUpdate = document.querySelector(`.chat-session-item[data-session-id="${sessionId}"]`);
      if (sessionItemToUpdate) {
        const titleElement = sessionItemToUpdate.querySelector('.session-title');
        if (titleElement) {
          titleElement.textContent = data.new_title;
        }
      }
    }
  } catch (error) {
    console.error('Error updating title:', error);
  }
}

function appendMessage(sender, message) {
  console.log(`Appending message: [${sender}] ${message}`);
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);
  messageElement.innerHTML = marked.parse(message);
  chatMain.appendChild(messageElement);

  // ✅ 페이지 전체를 아래로 자동 스크롤
  scrollToBottom();
}

function scrollToBottom() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
