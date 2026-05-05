document.getElementById('start_date').addEventListener('change', function () {
    const selectedDateValue = this.value;
    const timeSelectionSection = document.getElementById('timeSelectionSection');
    const nextButton = document.getElementById('nextButton');

    console.log('Date changed to:', selectedDateValue);

    if (selectedDateValue) {
        timeSelectionSection.classList.remove('hidden');
        console.log('Showing time selection section');
    } else {
        timeSelectionSection.classList.add('hidden');
        nextButton.disabled = true;
        return;
    }

    const facilityId = typeof location_id !== 'undefined' ? location_id : null;
    const selectedDate = new Date(selectedDateValue);
    const currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0);

    const now = new Date();
    const currentHours = now.getHours();

    const timeButtons = document.querySelectorAll('.time-slot');

    // Reset all buttons
    timeButtons.forEach(button => {
        button.disabled = false;
        button.classList.remove('disabled', 'active');
    });

    // 1. Check if past date
    if (selectedDate < currentDate) {
        alert("ไม่สามารถจองวันที่ในอดีตได้!");
        this.value = '';
        timeSelectionSection.classList.add('hidden');
        return;
    }

    // 2. Check if today (disable past hours)
    // AND check business hours
    timeButtons.forEach(button => {
        const buttonTimeStr = button.getAttribute('data-time'); // e.g., "09:00:00"
        const buttonHour = parseInt(buttonTimeStr.split(':')[0], 10);
        
        // Check past hours if today
        if (selectedDate.toDateString() === now.toDateString()) {
            if (buttonHour <= currentHours) {
                button.disabled = true;
                button.classList.add('disabled');
                return;
            }
        }

        // Check business hours
        if (typeof openingHour !== 'undefined' && typeof closingHour !== 'undefined') {
            const openH = parseInt(openingHour.split(':')[0], 10);
            const closeH = parseInt(closingHour.split(':')[0], 10);
            
            if (buttonHour < openH || buttonHour >= closeH) {
                button.disabled = true;
                button.classList.add('disabled');
            }
        }
    });

    // Fetch booked slots
    fetch('/book-first/check-available-times/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            date: selectedDateValue,
            facility_id: facilityId
        })
    })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Booked slots received:', data);
            data.forEach(bookedTime => {
                const timeStr = bookedTime.time_reserve;
                const timeButton = document.querySelector(`.time-slot[data-time="${timeStr}"]`);
                if (timeButton) {
                    timeButton.disabled = true;
                    timeButton.classList.add('disabled');
                    console.log('Disabled slot:', timeStr);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching available times:', error);
            // Optionally show error to user
        });
});

// Use event delegation for time slot selection to handle dynamic updates
document.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('time-slot')) {
        const button = e.target;
        if (button.classList.contains('disabled')) return;

        console.log('Time slot selected:', button.getAttribute('data-time'));

        // Remove active from all
        document.querySelectorAll('.time-slot').forEach(btn => btn.classList.remove('active'));

        // Add active to selected
        button.classList.add('active');

        // Update hidden input
        document.getElementById('selected_time').value = button.getAttribute('data-time');

        // Enable next button
        document.getElementById('nextButton').disabled = false;
    }
});