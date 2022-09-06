window.addEventListener("load", () => {
    console.log(1);
    if (location.href.split("/").includes("note")) initEdit();
});

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
}