  function saveScrollPosition() {
    localStorage.setItem("scrollPosition", window.scrollY);
  }

  window.onload = function () {
    if (localStorage.getItem("scrollPosition")) {
      window.scrollTo(0, localStorage.getItem("scrollPosition"));
      localStorage.removeItem("scrollPosition");
    }
  };
  const dayNames = ["нд", "пн", "вт", "ср", "чт", "пт", "сб"];
  const dayRows = document.querySelectorAll(".day-row");

  dayRows.forEach((row) => {
    const dayNumber = parseInt(row.getAttribute("data-day"), 10);
    if (!isNaN(dayNumber)) {
      const today = new Date();
      const year = today.getFullYear();
      const month = today.getMonth();
      const date = new Date(year, month, dayNumber);
      const dayName = dayNames[date.getDay()];
      row.querySelector(".day-name").textContent = dayName;
    }
  });


  function showModal(message, logId, action) {
    saveScrollPosition();

    const modal = document.getElementById("confirmationModal");
    const modalText = document.getElementById("modal-text");
    const confirmButton = document.getElementById("confirmButton");
    modalText.textContent = message;

    let formSelector;
    if (action === "delete") {
      formSelector = `form[action="/delete_log/${logId}/"]`;
    } else if (action === "change") {
      formSelector = `form[action="/change_bonus/${logId}/"]`;
    }

    confirmButton.onclick = function () {
      const form = document.querySelector(formSelector);
      if (form) {
        form.submit();
      } else {
        alert("Форма не знайдена");
      }
      closeModal();
    };

    modal.style.display = "block";
  }

  function closeModal() {
    const modal = document.getElementById("confirmationModal");
    modal.style.display = "none";
  }

  document.addEventListener("DOMContentLoaded", function () {
    const dayRows = document.querySelectorAll(".day-row");
  
    dayRows.forEach((row) => {
      const topRow = row.querySelector(".day-row-top");
  
      if (topRow) {
        row.addEventListener("click", function () {
          dayRows.forEach((otherRow) => {
            const otherTopRow = otherRow.querySelector(".day-row-top");
            if (otherTopRow && otherTopRow !== topRow && otherTopRow.classList.contains("show")) {
              otherTopRow.classList.remove("show");
            }
          });
  
          if (topRow.classList.contains("show")) {
            topRow.classList.remove("show");
          } else {
            topRow.classList.add("show");
          }
        });
      }
    });
  });
  
  document.addEventListener("DOMContentLoaded", function () {
    const dayNames = ["нд", "пн", "вт", "ср", "чт", "пт", "сб"];
    const dayRows = document.querySelectorAll(".day-row");

    // Отримуємо параметри місяця та року з URL або використовуємо поточну дату
    const urlParams = new URLSearchParams(window.location.search);
    let year = parseInt(urlParams.get('year'), 10);
    let month = parseInt(urlParams.get('month'), 10);

    // Якщо параметри не задані, використовуємо поточний рік і місяць
    const currentDate = new Date();
    if (isNaN(year)) {
        year = currentDate.getFullYear();
    }
    if (isNaN(month)) {
        month = currentDate.getMonth() + 1; // Місяці в URL передаються з 1 (січень = 1)
    }

    dayRows.forEach((row) => {
        const dayNumber = parseInt(row.getAttribute("data-day"), 10);
        if (!isNaN(dayNumber)) {
            // Створюємо дату для конкретного дня
            const date = new Date(year, month - 1, dayNumber); // Місяці в JavaScript рахуються з 0
            const dayName = dayNames[date.getDay()];
            row.querySelector(".day-name").textContent = dayName;

            // Додаємо клас для вихідних днів (субота та неділя)
            if (date.getDay() === 0 || date.getDay() === 6) {
                row.classList.add("weekend-day");
            } else {
                row.classList.remove("weekend-day");
            }
        }
    });
});
