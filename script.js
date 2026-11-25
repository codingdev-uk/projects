const clockEl = document.getElementById('clock');
const dateEl = document.getElementById('date');
const tzSelect = document.getElementById('timezone-select');

// Automatically label the first option with the user's detected local city
const localTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
const localCity = localTimezone.split('/').pop().replace(/_/g, ' ');
tzSelect.options[0].textContent = `Local (${localCity})`;

let activeTimezone = localTimezone;
let timerId = null;

function updateClock() {
  const now = new Date();

  const timeFormatter = new Intl.DateTimeFormat('en-GB', {
    timeZone: activeTimezone,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  clockEl.textContent = timeFormatter.format(now);

  const dateFormatter = new Intl.DateTimeFormat('en-GB', {
    timeZone: activeTimezone,
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
  dateEl.textContent = dateFormatter.format(now);

  // Sync tightly with the next real-world second
  const delay = 1000 - now.getMilliseconds();
  timerId = setTimeout(updateClock, delay);
}

tzSelect.addEventListener('change', (e) => {
  activeTimezone = e.target.value === 'local' ? localTimezone : e.target.value;
  clearTimeout(timerId);
  updateClock();
});

updateClock();
