var typed = new Typed('.typing-text', {
    strings: ['Empower your routine','Optimize your day', 'Stay ahead with real-time updates','Get a personal Dashboard','And achieve more'],
    typeSpeed: 50,
    backSpeed: 50,
    backDelay: 1000,
    loop: true,
    
});

let quoteIndex = 0;

function changeQuote() {
    const introElement = document.getElementsByClassName('starts');
    
}

// Change the quote every 5 seconds
setInterval(changeQuote, 5000);


/*for schedule section*/

document.addEventListener("DOMContentLoaded", function () {
    // Fetch and display routine on page load
    fetchRoutine("All");

    // Handle day button clicks
    document.querySelectorAll(".days-list li").forEach(dayBtn => {
        dayBtn.addEventListener("click", function () {
            let selectedDay = this.getAttribute("data-filter");

            // Update active button
            document.querySelector(".days-list .active").classList.remove("active");
            this.classList.add("active");

            // Fetch and display routine for the selected day
            fetchRoutine(selectedDay);
        });
    });
});

// Function to fetch and display routine
function fetchRoutine(filterDay) {
    fetch("/get_schedule/")  // Django API endpoint
        .then(response => response.json())
        .then(data => {
            displaySchedule(data.schedule, filterDay);
        })
        .catch(error => console.error("Error fetching schedule:", error));
}

// Function to display the routine table based on the selected day
function displaySchedule(scheduleData, filterDay) {
    let tableBody = document.getElementById("schedule-body");
    tableBody.innerHTML = ""; // Clear previous data

    let facultyData = {}; // Object to store faculty-wise schedules

    // Organize data by faculty
    scheduleData.forEach(schedule => {
        if (filterDay === "All" || schedule.day === filterDay) {
            if (!facultyData[schedule.faculty_name]) {
                facultyData[schedule.faculty_name] = {}; // Create an entry if not exists
            }
            facultyData[schedule.faculty_name][schedule.period] = 
                `${schedule.subject} <br> ${schedule.section} <br> Room ${schedule.room_no}`;
        }
    });

    // Generate table rows
    for (let faculty in facultyData) {
        let row = `<tr><td><strong>${faculty}</strong></td>`;

        // Loop through periods (1-6)
        for (let i = 1; i <= 6; i++) {
            row += `<td>${facultyData[faculty][i] || "—"}</td>`; // If no schedule, show "—"
        }

        row += `</tr>`;
        tableBody.innerHTML += row;
    }
}
