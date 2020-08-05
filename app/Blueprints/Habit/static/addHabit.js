const addHabitButton = document.getElementById('add-habit-button');
const addHabitForm = document.getElementById('add-habit-form');
addHabitButton.addEventListener('click', () => {
    addHabitButton.hidden = true;
    addHabitForm.hidden = false;
})