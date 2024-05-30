const mainForm =  document.querySelector("form")
const userInput = document.getElementById("nlp_request")
const chat = document.getElementById("chat")

const addMsgToChat = function(text){

    newMsg = document.createElement("h1")
    newMsg.class = "chatMsg"
    newMsg.textContent = text

    chat.appendChild(newMsg)

}

mainForm.addEventListener("submit",async (event)=>{
    event.preventDefault()
    
    if(userInput.value == "") return

    addMsgToChat(userInput.value)

    let request = await fetch(mainForm.action)
    let response = await request.json()
    let nlpMsg = response.nlpResponse
    
    addMsgToChat(nlpMsg)
})