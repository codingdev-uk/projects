const clockEl = document.getElementById('clock');
const dateEl = document.getElementById('date');
const timezoneEl = document.getElementById('timezone');

// Detect user's local timezone once on load
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
timezoneEl.textContent = userTimezone;

function updateRealTimeClock() {
  const now = new Date();

  // Format hours, minutes, and seconds
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  clockEl.textContent = `${hours}:${minutes}:${seconds}`;

  // Format current day and date
  const dateOptions = { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  };
  dateEl.textContent = now.toLocaleDateString(undefined, dateOptions);

  // Sync the next update to the exact start of the next second
  const delayUntilNextSecond = 1000 - now.getMilliseconds();
  setTimeout(updateRealTimeClock, delayUntilNextSecond);
}

// Start the clock
updateRealTimeClock();
