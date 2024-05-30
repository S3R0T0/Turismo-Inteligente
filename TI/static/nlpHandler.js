const mainForm =  document.querySelector("form")
const userInput = document.getElementById("nlp_request")
const chat = document.getElementById("chat")
console.log("A")
const addMsgToChat = function(text,cls){

    console.log("ee")

    newMsg = document.createElement("h1")
    newMsg.classList.add(cls)
    newMsg.textContent = text

    chat.appendChild(newMsg)

}

mainForm.addEventListener("submit",async (event)=>{
    event.preventDefault()
    
    if(userInput.value == "") return

    addMsgToChat(userInput.value,"chatMsg")

    let request = await fetch(mainForm.action+`?nlp_request=${userInput.value}`)
    let response = await request.json()
    let nlpMsg = response.nlpResponse
    
    addMsgToChat(nlpMsg,"chatResponse")
})