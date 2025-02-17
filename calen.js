import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        events: [
            { title: 'Event 1', start: '2023-02-01' },
            { title: 'Event 2', start: '2023-02-07', end: '2023-02-10' }
        ]
    });

    calendar.render();
});
