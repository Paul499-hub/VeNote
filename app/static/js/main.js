// Templates
const searchResultTemplate = document.getElementById("search-result-template")
const cancelUpdateTemplate = document.getElementById("cancel_btn_template")
const textareaTemplate = document.getElementById("textarea_template")
const saveBtnTemplate = document.getElementById("save_btn_template")
// HTML elements
const searchNoteSQLBtnEl = document.getElementById("search-note-sql-btn")
const searchNoteBtnEl = document.getElementById("search-note-btn") // vector search
const searchResultsEl = document.getElementById("search-results") // search results parent div
const saveNoteBtnEl = document.getElementById("save-note-btn")
const noteInputEl = document.getElementById("main_note_input")

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

// Helper function to convert search result data to html cards
function display_found_cards_HTML(data){
    // data =  list of dicts with keys
    // "id": n.id,
    // "score": memory[n.id],
    // "text": n.text,
    // "html_md" : parse_into_markdown(n.text), 
    // >> this was from vector search
    console.log(data)
    searchResultsEl.innerHTML = "";
    data.forEach( (item, index)=>{
        const fragment = searchResultTemplate.content.cloneNode(true);
        const cardEl = fragment.querySelector("#card")
        // write markdown into card-content
        fragment.querySelector(".card-content").innerHTML = item.html_md
        // Delete button and it's event listener
        const del_btn = fragment.getElementById("del_note")
        const noteId = item.id
        const raw_text = item.text
        // store useful data inside card's dataset 
        cardEl.dataset.noteId = item.id;
        cardEl.dataset.rawText = item.text;
        cardEl.dataset.htmlMd = item.html_md;
        // add event listeners 
        add_event_listener_on_delete_btn(del_btn, noteId);
        add_event_listener_on_update_note_btn2(cardEl, noteId, raw_text);
        searchResultsEl.appendChild(fragment);
    })
}



function add_event_listener_on_delete_btn(btn, noteId){
    btn.onclick = async(event) => {
        const savedCard = event.currentTarget.closest("#card") 
        const response = await fetch(`/storage/del/${noteId}`, {
            method: "DELETE",
        });
        if(!response.ok){
            const err = await response.json();
            alert(err.detail || "Delete failed");
            return;
        }
        const result = await response.json();
        alert("❌ Note deleted");
        savedCard.remove(); // !! IMPORTANT events becomes null after await 
    }
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
    const response = await fetch("/storage/similarity_search", {
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

function add_event_listener_on_update_note_btn2(cardEl, noteId, raw_text){
    const update_btn = cardEl.querySelector("#update_note");
    const update_wrapperEl = update_btn.closest(".btn_wrapper"); 
    update_btn.onclick = async(event) => {
        // save old card state
        const savedCardEl = event.currentTarget.closest("#card").cloneNode(true);
        // remove el with class .card-content
        const parentCardEl = event.currentTarget.closest("#card")
        const allButtonsEl = event.currentTarget.closest(".all_buttons")
        const cardContentEl = parentCardEl.querySelector(".card-content");
        cardContentEl.innerHTML = ''
        // add new textarea using template
        const clonedTextareaTemplate = textareaTemplate.content.cloneNode(true);
        const clonedSaveBtnTemplate = saveBtnTemplate.content.cloneNode(true);
        const clonedCancelUpdateTemplate = cancelUpdateTemplate.content.cloneNode(true);
        // gather textarea / save elements
        const clonedTextareaEl = clonedTextareaTemplate.querySelector('#note_input')
        const clonedSaveBtnEl = clonedSaveBtnTemplate.querySelector("#save_note")
        const clonedCancelBtnEl = clonedCancelUpdateTemplate.querySelector("#cancel_update")
        // replace text from routes raw text output 'text'
        clonedTextareaEl.value = raw_text
        cardContentEl.appendChild(clonedTextareaTemplate)
        // Expand textarea
        clonedTextareaEl.style.boxSizing = "border-box"
        clonedTextareaEl.style.height = `${clonedTextareaEl.scrollHeight}px`
        // add new buttons
        allButtonsEl.appendChild(clonedSaveBtnTemplate)
        allButtonsEl.appendChild(clonedCancelUpdateTemplate)
        // remove update note button
        update_wrapperEl.remove();
        // add event listeners to new buttons
        add_event_listener_on_save_btn(clonedSaveBtnEl, noteId, clonedTextareaEl)
        add_event_listener_on_cancel_update_btn(clonedCancelBtnEl, savedCardEl)
    }
}

function add_event_listener_on_save_btn(save_btn, noteId, clonedTextareaEl){
    save_btn.onclick = async(event) => {
        // read text from new textarea
        const text = clonedTextareaEl.value.trim()
        const closest_card3 = event.currentTarget.closest(".card3")
        const response = await fetch("/storage/update_note", {
            method: "PATCH",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({"id":noteId, "text":text})
        });
        if (!response.ok){
            const err = await response.json();
            alert(err.detail || "Update failed");
            return;
        }
        const result = await response.json();
        alert("✨ Note updated");
        await replace_single_card(noteId, closest_card3)
    }
}

async function replace_single_card(noteId, replaceTargetEl){
    // Refresh the note - get new parsed text by sql fetch by id /sqlite/get_note/{note_id}
        const response = await fetch(`/sqlite/get_note/${noteId}`, {method: "GET"});
        if (!response.ok){
            alert("Note was saved but could not be refreshed in UI")
            return;
        }
        const data = await response.json();
        // return {
        //     "id": note.id,
        //     "score": 1.0,
        //     "text": note.text,
        //     "html_md": parse_into_markdown(note.text)
        // }
        // Create textarea , all_buttons(delete, update)
        const fragment = searchResultTemplate.content.cloneNode(true);
        const cardEl = fragment.querySelector(".card3")
        const raw_text = data.text
        // write markdown into card-content
        fragment.querySelector(".card-content").innerHTML = data.html_md
        // Delete button
        const del_btn = fragment.getElementById("del_note")
        add_event_listener_on_delete_btn(del_btn, data.id);
        // Update button (already created in fragment)
        add_event_listener_on_update_note_btn2(cardEl, data.id, raw_text);
        // store useful data inside card's dataset 
        cardEl.dataset.noteId = data.id;
        cardEl.dataset.rawText = data.text;
        cardEl.dataset.htmlMd = data.html_md;
        replaceTargetEl.replaceWith(fragment)
}

function add_event_listener_on_cancel_update_btn(btn, savedCardEl){
    btn.onclick = async(event) => {
        const currentCard = event.currentTarget.closest("#card")
        // replace card with new one (already cloned)
        currentCard.replaceWith(savedCardEl) //currentCard becomes outdated/old here
        // get required data
        const del_btn = savedCardEl.querySelector("#del_note")
        const noteId = currentCard.dataset.noteId;
        const raw_text = currentCard.dataset.rawText;
        // add event listeners 
        add_event_listener_on_delete_btn(del_btn, noteId);
        add_event_listener_on_update_note_btn2(savedCardEl, noteId, raw_text);
    }
}

function print_fragment(fragment){
    const temp = document.createElement("div");
    temp.appendChild(fragment.cloneNode(true));
    console.log(temp.innerHTML);
}
