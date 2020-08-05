const verifyResponse = (data) => {
    if (data.status === 1) {
        return true;
    }
    return false;
}

const clientSideDeleteTask = (id) => {
    const divToDelete = document.getElementById(id);

    divToDelete.parentNode.removeChild(divToDelete);
}

const deleteTask = (id) => {
    fetch('/task/delete', {
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
        if (verifyResponse(data)) {
            clientSideDeleteTask(id);
        } else {
            console.log(data)
        }
      })
}