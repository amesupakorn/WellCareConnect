
document.getElementById('confirmButton').addEventListener('click', function() {
        const bookDate = document.getElementById('bookDate').textContent.trim();
        const bookTime = document.getElementById('bookTime').textContent.trim();
        const symptoms = document.getElementById('symptoms').textContent.trim();
        const bookerName = document.getElementById('bookerName').textContent.trim();
        const phone = document.getElementById('phone').textContent.trim();

        const data = {
            booker: bookerName,
            phone: phone,
            symptoms: symptoms,
            date_reserve: bookDate,
            time_reserve: bookTime,
            location: location_id
        };

        fetch('confirm/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                localStorage.setItem('bookingSuccess', 'บันทึกการจองของคุณเรียบร้อย');
                window.location.href = '/book-list';
            } else {
                alert('There was an error with the booking: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

