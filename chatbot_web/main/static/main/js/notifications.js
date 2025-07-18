// notifications.js

document.addEventListener('DOMContentLoaded', function() {
    const notificationBellPC = document.getElementById('notificationBellPC');
    const notificationCountBadgePC = document.getElementById('notificationCountBadgePC');
    const notificationDropdownPC = document.getElementById('notificationDropdownPC');

    const notificationBellMobile = document.getElementById('notificationBellMobile');
    const notificationCountBadgeMobile = document.getElementById('notificationCountBadgeMobile');
    const notificationDropdownMobile = document.getElementById('notificationDropdownMobile');

    // Function to fetch notifications
    async function fetchNotifications() {
        try {
            const response = await fetch('/api/notifications/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            const notifications = data.notifications;
            const unreadCount = notifications.length;

            // Update badges
            [notificationCountBadgePC, notificationCountBadgeMobile].forEach(badge => {
                if (badge) {
                    if (unreadCount > 0) {
                        badge.textContent = unreadCount;
                        badge.classList.remove('d-none');
                    } else {
                        badge.classList.add('d-none');
                    }
                }
            });

            // Populate dropdowns
            [notificationDropdownPC, notificationDropdownMobile].forEach(dropdown => {
                if (dropdown) {
                    dropdown.innerHTML = ''; // Clear previous notifications
                    if (notifications.length === 0) {
                        const noNotifItem = document.createElement('li');
                        noNotifItem.innerHTML = '<a class="dropdown-item" href="#">알림이 없습니다.</a>';
                        dropdown.appendChild(noNotifItem);
                    } else {
                        notifications.forEach(notif => {
                            const notifItem = document.createElement('li');
                            const notifLink = document.createElement('a');
                            notifLink.classList.add('dropdown-item');
                            notifLink.href = notif.link || '#'; // Link to the notification source
                            notifLink.textContent = notif.message;
                            notifLink.dataset.notificationId = notif.id; // Store notification ID
                            notifLink.addEventListener('click', async (e) => {
                                e.preventDefault();
                                await markNotificationAsRead(notif.id);
                                if (notif.link) {
                                    window.location.href = notif.link;
                                }
                            });
                            notifItem.appendChild(notifLink);
                            dropdown.appendChild(notifItem);
                        });
                    }
                }
            });

        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    }

    // Fetch notifications on page load
    if (notificationBellPC || notificationBellMobile) {
        fetchNotifications();
        setInterval(fetchNotifications, 30000); // Poll for new notifications every 30 seconds
    }

    // Function to mark notification as read
    async function markNotificationAsRead(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            // Re-fetch notifications to update count
            fetchNotifications();
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }

    // Helper to get CSRF token
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
});