// DOM Elements
const userIdInput = document.getElementById('user-id-input');
const loadNotificationsBtn = document.getElementById('load-notifications-btn');
const notificationsList = document.getElementById('notifications-list');
const notificationCount = document.getElementById('notification-count');
const loadingEl = document.getElementById('loading');
const emptyStateEl = document.getElementById('empty-state');
const apiErrorEl = document.getElementById('api-error');

// API URL
const API_URL = 'http://localhost:5003';

// Event listeners
loadNotificationsBtn.addEventListener('click', fetchNotifications);

// Fetch notifications when page loads with default user ID
document.addEventListener('DOMContentLoaded', fetchNotifications);

// Format time ago
function timeAgo(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.round((now - date) / 1000);
  const minutes = Math.round(seconds / 60);
  const hours = Math.round(minutes / 60);
  const days = Math.round(hours / 24);
  
  if (seconds < 60) return 'just now';
  if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
  if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`;
  return date.toLocaleDateString();
}

// Fetch notifications from API
async function fetchNotifications() {
  const userId = userIdInput.value.trim();
  
  if (!userId) {
    alert('Please enter a User ID');
    return;
  }
  
  // Show loading
  loadingEl.style.display = 'block';
  emptyStateEl.style.display = 'none';
  notificationsList.innerHTML = '';
  apiErrorEl.style.display = 'none';
  
  try {
    const response = await fetch(`${API_URL}/notifications/${userId}`);
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const notifications = await response.json();
    displayNotifications(notifications);
  } catch (error) {
    console.error('Failed to fetch notifications:', error);
    apiErrorEl.style.display = 'block';
  }
}

// Display notifications in the UI
function displayNotifications(notifications) {
  // Hide loading
  loadingEl.style.display = 'none';
  
  // Update notification count
  notificationCount.textContent = `${notifications.length} notification${notifications.length !== 1 ? 's' : ''}`;
  
  if (notifications.length === 0) {
    emptyStateEl.style.display = 'block';
    return;
  }
  
  // Add each notification to the list
  notifications.forEach(notification => {
    const card = document.createElement('div');
    card.className = 'notification-card';
    card.innerHTML = `
      <div class="notification-header-content">
        <strong>Booking #${notification.booking_id}</strong>
        <small>${timeAgo(notification.timestamp)}</small>
      </div>
      <p>${notification.message}</p>
    `;
    notificationsList.appendChild(card);
  });
}
