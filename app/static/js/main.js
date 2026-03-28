const noteInputEl = document.getElementById("note_input")
const saveNoteBtnEl = document.getElementById("save-note-btn")
const searchNoteBtnEl = document.getElementById("search-note-btn")
const searchResultsEl = document.getElementById("search-results")
const searchResultTemplate = document.getElementById("search-result-template")

saveNoteBtnEl.addEventListener("click", saveNote)
searchNoteBtnEl.addEventListener("click", searchNote)

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
    console.log(data)
    searchResultsEl.innerHTML = "";
    data.forEach( (item, index)=>{

        const fragment = searchResultTemplate.content.cloneNode(true);
        fragment.querySelector(".card-title").textContent = `#${index + 1}`;
        fragment.querySelector(".card-content").textContent = `${item.text}`;
        searchResultsEl.appendChild(fragment);

        // const resultEl = document.createElement("div")
        // resultEl.className = "search-result-el"
        // resultEl.innerHTML = `
        //     <div><strong>#${index + 1}</strong></div>
        //     <div><strong>Score:</strong>${item.score}</div>
        //     <div><strong>Text:</strong>${item.text}</div>
        // `;
        // searchResultsEl.appendChild(resultEl)
    })
}