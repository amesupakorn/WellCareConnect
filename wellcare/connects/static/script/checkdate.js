  // ฟังก์ชันคำนวณอายุ
  function calculateAgeAndMonths(day, month, year) {
    const today = new Date();
    const birthDate = new Date(year, month - 1, day); // เดือนใน JavaScript นับจาก 0
    let age = today.getFullYear() - birthDate.getFullYear();
    let months = today.getMonth() - birthDate.getMonth();
    const days = today.getDate() - birthDate.getDate();

    // ถ้าเดือนปัจจุบันน้อยกว่าเดือนเกิด หรือ เดือนเท่ากันแต่วันปัจจุบันน้อยกว่าวันเกิด
    if (months < 0 || (months === 0 && days < 0)) {
        age--;
        months += 12;
    }

    if (days < 0) {
        months--;
    }

    return { age, months };
}
// ฟังก์ชันคำนวณโปรเกรสเซอร์วงกลม
function setProgressCircle(percent) {
    const circle = document.querySelector('.progress');
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;

    const offset = circumference - (percent / 100) * circumference;
    circle.style.strokeDashoffset = offset;
}

// ฟังก์ชันตรวจสอบสิทธิ์และแสดงผล
function checkEligibility() {
    // รับค่าจาก URL
    const urlParams = new URLSearchParams(window.location.search);
    const day = urlParams.get('day');
    const month = urlParams.get('month');
    const year = urlParams.get('year');

    if (day && month && year) {
        const { age, months } = calculateAgeAndMonths(day, month, year); // ได้ทั้งอายุและเดือน
        document.getElementById("ageText").innerText = `อายุ ${age} ปี`;
        document.getElementById("monthsText").innerText = `${months} เดือน`; // แสดงจำนวนเดือนที่คำนวณได้

        // คำนวณเปอร์เซ็นต์ความสำเร็จ
        const percentComplete = (age / 60) * 100;  // สมมติว่าอายุสูงสุดที่ 60 ปี
        setProgressCircle(percentComplete);  // แสดงเปอร์เซ็นต์ในวงกลม

        // ตรวจสอบสิทธิ์ (ตัวอย่าง: หากอายุมากกว่า 60 ปี มีสิทธิ์)
        const eligibilityResult = document.getElementById("eligibility-result");
        if (age >= 60) {
            eligibilityResult.innerText = "ท่านมีสิทธิ์รับเบี้ยยังชีพผู้สูงอายุ";
            eligibilityResult.classList.add('text-green-500');  // เพิ่มสีเขียว
        } else {
            eligibilityResult.innerText = "ท่านยังไม่มีสิทธิ์รับเบี้ยยังชีพผู้สูงอายุ";
            eligibilityResult.classList.add('text-red-500');  // เพิ่มสีแดง
        }
    } else {
        alert("ไม่พบข้อมูลวันเกิด กรุณากรอกข้อมูลให้ครบถ้วน");
    }
}

window.onload = checkEligibility;
