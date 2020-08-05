const clientSideDeleteHabit = (id) => {
    const divToDelete = document.getElementById(id).parentNode;

    divToDelete.parentNode.removeChild(divToDelete);
}

const verifyResponse = (data) => {
    if (data.status === 1) {
        return true;
    }
    return false;
}

const deleteHabit = (id) => {
    fetch('/habit/delete', {
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
            clientSideDeleteHabit(id)
        } else {
            console.log(data)
        }
      })
}