window.addEventListener("load", () => {
    if (location.href.split("/").includes("note")) initEdit();
    if (location.pathname == "/") initIndex();
});

function initIndex() {
    for (let delButton of $(".note-prev-delete")){
        console.log();

        delButton.addEventListener("click", () => {
            $.ajax({
                url: "/note/" + delButton.parentElement.id.slice(5),
                method: "DELETE",
                success: (resp) => { location.reload(); },
                error: (resp) => { console.log(resp.responseJSON['error']); }
            });
        })
    }
}

function initEdit() {
    let editButton = document.getElementById("nav-edit");
    let titleElement = document.getElementById("note-title");
    let textElement = document.getElementById("note-text");
    let saveButton = document.getElementById("save-button");

    let editing = false;

    saveButton.style.display = "none";

    editButton.addEventListener("click", () => {

        if (editing){
            location.reload();
        }

        else {
            editing = true;
            editButton.innerText = "Cancel";
            editButton.style.color = "var(--red)";
            editButton.style.borderColor = "var(--red)";

            saveButton.style.display = "block";

            titleElement.contentEditable = true;
            textElement.contentEditable = true;
            titleElement.focus();
        }
    });

    saveButton.addEventListener("click", () => {
        $.ajax({
            url: location.pathname,
            method: "PUT",
            data: {
                "title": titleElement.textContent,
                "text": textElement.textContent
            },

            success: (resp) => { location.reload(); },
            error: (resp) => { 
                $.notify(resp.responseJSON['error']);
            }
        });

    });
}