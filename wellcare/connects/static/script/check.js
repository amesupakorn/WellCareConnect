function submitForm() {
    // ดึงค่าจาก dropdown
    const day = document.getElementById("day").value;
    const month = document.getElementById("month").value;
    const year = document.getElementById("year").value;

    if (day && month && year) {
        window.location.href = `showcheck?day=${day}&month=${month}&year=${year}`;
    } else {
        Swal.fire({
            icon: "error",
            title: "กรุณากรอกวันเดือนปีเกิดให้ครบถ้วน",
            confirmButtonText: 'ตกลง',
            confirmButtonColor: '#0066FF' 
          });
    }
}