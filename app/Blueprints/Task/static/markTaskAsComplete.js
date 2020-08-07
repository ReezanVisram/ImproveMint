const verifyTaskResponse = (data) => {
    if (data.status === 1) {
        return true;
    }
    return false;
}

const clientSideDeleteTask = (id) => {
    const divToDelete = document.getElementById(id);

    divToDelete.parentNode.removeChild(divToDelete);
}

const markTaskAsComplete = (id) => {
    fetch('/task/markAsComplete', {
        method: "POST",
        headers: new Headers({
            "Accept": "application/json",
            "Content-Type": "application/json"
        }),
        body: (
            JSON.stringify(
                {'id': id}
            )
        )
    }).then(response => response.json())
      .then(data => {
        if (verifyTaskResponse(data)) {
            clientSideDeleteTask(id);
        } else {
            console.log(data)
        }
      })
}