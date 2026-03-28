const noteInputEl = document.getElementById("note_input")
const saveNoteBtnEl = document.getElementById("save-note-btn")

saveNoteBtnEl.addEventListener("click", saveNote)

async function saveNote(){
    const text = noteInputEl.value.trim();
    if (!text){
        alert("Note text is empty!");
        return;
    }
    const response = await fetch( "/qdrant/store_note", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"text":text})
        }
    );
    const data = await response.json();
    alert( "✅ Note embedded and saved" )
}