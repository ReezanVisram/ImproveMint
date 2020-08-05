const addTaskButton = document.getElementById('add-task-button');

addTaskButton.addEventListener('click', () => {
    if (document.getElementById('add-task-form').hidden) {
        document.getElementById('add-task-form').hidden = false;
        addTaskButton.hidden = true;
    }
})