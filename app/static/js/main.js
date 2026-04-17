const searchResultTemplate = document.getElementById("search-result-template")
const searchNoteSQLBtnEl = document.getElementById("search-note-sql-btn")
const searchNoteBtnEl = document.getElementById("search-note-btn")
const searchResultsEl = document.getElementById("search-results")
const saveNoteBtnEl = document.getElementById("save-note-btn")
const noteInputEl = document.getElementById("note_input")

searchNoteBtnEl.addEventListener("click", searchNote)
saveNoteBtnEl.addEventListener("click", saveNote)
searchNoteSQLBtnEl.addEventListener("click", searchNoteSQL)
noteInputEl.addEventListener('keydown', function(e) {
  if (e.key === 'Tab') {
    // 1. Prevent the default "move focus" behavior
    e.preventDefault();
    // 2. Get current cursor position
    const start = this.selectionStart;
    const end = this.selectionEnd;
    // 3. Set textarea value to: text before + tab + text after
    this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
    // 4. Put the cursor back in the right place (after the tab)
    this.selectionStart = this.selectionEnd = start + 1;
  }
});

//  /storage/update_note  -> id text

// Helper function to convert search result data to html cards
function display_found_cards_HTML(data){
    console.log(data)
    searchResultsEl.innerHTML = "";
    data.forEach( (item, index)=>{
        const fragment = searchResultTemplate.content.cloneNode(true);
        //fragment.querySelector(".card-title").textContent = `#${index + 1}`;
        //fragment.querySelector(".card-content").textContent = `${item.text}`;
        fragment.querySelector(".card-content").innerHTML = item.html_md
        // Delete button and it's event listener
        const del_btn = fragment.getElementById("del_note")
        const noteId = item.id
        del_btn.onclick = async (event) => {
            const response = await fetch(`/storage/del/${noteId}`, {
                method: "DELETE",
            });
            if (!response.ok) {
                const err = await response.json();
                alert(err.detail || "Delete failed");
                return;
            }
            const result = await response.json();
            alert("❌ Note deleted");
            event.currentTarget.closest(".parent").remove();
        }
        // Update button and it's event listener
        const update_btn = fragment.getElementById("update_note")
        update_btn.onclick = async(event) => {
            const text = noteInputEl.value.trim();
            if (!text){
                alert("Note text is empty!");
                return;
            }
            console.log({ id: noteId, text });
            const response = await fetch('/storage/update_note', {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({"id": noteId, "text":text})
            });
            if (!response.ok){
                const err = await response.json();
                alert(err.detail || "Update failed");
                return;
            }
            const result = await response.json();
            alert("✨ Note updated");
        }
        searchResultsEl.appendChild(fragment);
    })
}

async function saveNote(){
    const text = noteInputEl.value.trim();
    if (!text){
        alert("Note text is empty!");
        return;
    }
    const response = await fetch( "/storage/save_note", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"text":text})
        }
    );
    if (!response.ok) {
        const err = await response.json();
        alert(err.detail || "Request failed");
        return;
    }
    const data = await response.json();
    alert( "✅ Note embedded and saved" )
}

async function searchNote(){
    const text = noteInputEl.value.trim();
    if (!text){
        alert("Note text is empty!");
        return;
    }
    const response = await fetch("/qdrant/similarity_search", {
            method: "POST",
            headers: {"Content-Type": "application/json"}, //application/x-www-form-urlencoded
            body: JSON.stringify({"text":text, "args_limit":5}) ,
        }
    );
    const data = await response.json();
    display_found_cards_HTML(data)
}

async function searchNoteSQL(){
    const text = noteInputEl.value.trim()
    if (!text){
        alert("Note text is empty!");
        return;
    }
    const response = await fetch("/sqlite/get", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({"text":text})
    })
    const data = await response.json();
    display_found_cards_HTML(data)
}

