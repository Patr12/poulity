document.addEventListener('DOMContentLoaded', function() {
    // Initialize calendar
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: [
            {% for event in events %}
            {
                title: '{{ event.title }}',
                start: '{{ event.start|date:"Y-m-d" }}',
                {% if event.end %}
                end: '{{ event.end|date:"Y-m-d" }}',
                {% endif %}
                color: '{{ event.color }}',
                extendedProps: {
                    description: '{{ event.description }}',
                    type: '{{ event.type }}'
                }
            },
            {% endfor %}
        ],
        eventClick: function(info) {
            alert(
                info.event.title + '\n\n' +
                'Date: ' + info.event.start.toLocaleDateString() + '\n' +
                'Description: ' + info.event.extendedProps.description
            );
        }
    });
    calendar.render();

    // Navigation buttons
    document.getElementById('prev-month').addEventListener('click', function() {
        calendar.prev();
    });
    document.getElementById('next-month').addEventListener('click', function() {
        calendar.next();
    });
    document.getElementById('today').addEventListener('click', function() {
        calendar.today();
    });

    // Event filtering
    const filterCheckboxes = document.querySelectorAll('.event-filter');
    filterCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const eventType = this.dataset.type;
            const isChecked = this.checked;
            
            calendar.getEvents().forEach(function(event) {
                if (event.extendedProps.type === eventType) {
                    event.setProp('display', isChecked ? 'auto' : 'none');
                }
            });
            
            // Also filter the upcoming events list
            document.querySelectorAll('.event-item').forEach(function(item) {
                if (item.dataset.type === eventType) {
                    item.style.display = isChecked ? 'flex' : 'none';
                }
            });
        });
    });
});