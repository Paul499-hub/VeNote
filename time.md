## Todos
make notes vector variant ready 
document support for note (SQLite blob)
re-ranking
tunable limit


**QdrantService.similarity_search**
What needs to change. Qdrant gets a note id, score, text
text = sqlite id - id of sqlite row of original text
old text stored a COPY of original text - effectively doubling storage
Now source of truth will be SQLite - qdrant will only store vectors + references to object
We need to change what's stored into this text variable
After that the plan is to vector search like this 
- 1. Find most relevant vector's 
- 2. Fetch their corresponding SQLite rows by `text` stored in Qdrant
- 3. Extract text from SQLite
parse text like i currently do
```
"html_md": parse_into_markdown(s.payload.get('text')) if s.payload else None, 
```

StorageService.update_note can fail and leave vectordb not matching with sqlite.
If operation fails - add a user inidcation to rebuild.
