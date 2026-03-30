document.addEventListener("DOMContentLoaded",()=>{
  loadTopics();
  document.getElementById("query").addEventListener("keydown",(e)=>{
    if(e.key==="Enter")getRecommendations();
  });
});

async function loadTopics(){
  try{
    const res=await fetch("/topics");
    const data=await res.json();
    const grid=document.getElementById("topicsGrid");
    grid.innerHTML="";
    data.topics.slice(0,24).forEach(topic=>{
      const pill=document.createElement("button");
      pill.className="topic-pill";
      pill.textContent=topic;
      pill.onclick=()=>fillQuery(topic);
      grid.appendChild(pill);
    });
  }catch(e){console.warn("Could not load topics:",e);}
}

function fillQuery(text){
  document.getElementById("query").value=text;
  document.getElementById("query").focus();
}

async function getRecommendations(){
  const query=document.getElementById("query").value.trim();
  const level=document.getElementById("level").value;
  if(!query){showError("Please enter a search query.");return;}
  setLoading(true);hideAll();
  try{
    const res=await fetch("/recommend",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({query,level})
    });
    const data=await res.json();
    if(!res.ok||data.error){showError(data.error||"Something went wrong.");return;}
    renderResults(data);
  }catch(e){
    showError("Network error. Make sure Flask server is running.");
  }finally{setLoading(false);}
}

function renderResults(data){
  const{books,topic_label,ai_explanation,query,level}=data;
  if(ai_explanation){
    document.getElementById("aiTopic").textContent=`Topic: ${topic_label}`;
    document.getElementById("aiText").textContent=ai_explanation;
    document.getElementById("aiBox").classList.remove("hidden");
  }
  const metaText=level!=="All"?`${books.length} books · ${level} · "${query}"` : `${books.length} books · "${query}"`;
  document.getElementById("resultsMeta").textContent=metaText;
  const grid=document.getElementById("booksGrid");
  grid.innerHTML="";
  books.forEach((book,i)=>grid.appendChild(createBookCard(book,i+1)));
  document.getElementById("resultsSection").classList.remove("hidden");
  document.getElementById("resultsSection").scrollIntoView({behavior:"smooth",block:"start"});
}

function createBookCard(book,rank){
  const card=document.createElement("div");
  card.className="book-card";
  card.style.animationDelay=`${(rank-1)*0.08}s`;
  const cover=book.cover_url
    ?`<img class="book-cover" src="${book.cover_url}" alt="${book.title}" onerror="this.outerHTML='<div class=book-cover-placeholder>📖</div>'">`
    :`<div class="book-cover-placeholder">📖</div>`;
  const authors=book.authors?.join(", ")||"Unknown Author";
  const year=book.year!=="N/A"?`📅 ${book.year}`:"";
  const pages=book.pages!=="N/A"&&book.pages?`📄 ${book.pages} pages`:"";
  const rating=book.rating?`⭐ ${book.rating}`:"";
  const title=book.ol_url?`<a href="${book.ol_url}" target="_blank">${book.title}</a>`:book.title;
  const levelClass=`tag-level-${book.level||"Intermediate"}`;
  const subjectTags=(book.subjects||[]).filter(s=>s.length<40).slice(0,3).map(s=>`<span class="tag">${s}</span>`).join("");
  card.innerHTML=`
    <div class="book-rank">${rank}</div>
    ${cover}
    <div class="book-info">
      <div class="book-title">${title}</div>
      <div class="book-authors">by ${authors}</div>
      <div class="book-tags"><span class="tag ${levelClass}">${book.level||"Intermediate"}</span>${subjectTags}</div>
      <div class="book-meta">
        ${rating?`<span class="book-rating">${rating}</span>`:""}
        ${year}${pages}
      </div>
      <button class="similar-btn" onclick="getSimilar('${escapeQuotes(book.title)}')">Find Similar Books →</button>
    </div>`;
  return card;
}

async function getSimilar(title){
  try{
    const res=await fetch("/similar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title})});
    const data=await res.json();
    if(data.error||!data.books?.length)return;
    const section=document.getElementById("similarSection");
    const grid=document.getElementById("similarGrid");
    grid.innerHTML="";
    document.querySelector(".similar-title").textContent=`📖 Similar to "${title}"`;
    data.books.forEach((book,i)=>grid.appendChild(createBookCard(book,i+1)));
    section.classList.remove("hidden");
    section.scrollIntoView({behavior:"smooth",block:"start"});
  }catch(e){console.warn("Could not load similar books:",e);}
}

function setLoading(state){
  document.getElementById("btn-text").textContent=state?"Searching...":"Recommend";
  document.getElementById("btn-spinner").classList.toggle("hidden",!state);
}
function hideAll(){
  document.getElementById("resultsSection").classList.add("hidden");
  document.getElementById("similarSection").classList.add("hidden");
  document.getElementById("aiBox").classList.add("hidden");
  document.getElementById("errorBox").classList.add("hidden");
}
function showError(msg){
  const box=document.getElementById("errorBox");
  document.getElementById("errorText").textContent=msg;
  box.classList.remove("hidden");
}
function escapeQuotes(str){return str.replace(/'/g,"\\'").replace(/"/g,"&quot;");}