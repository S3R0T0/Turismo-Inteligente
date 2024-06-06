const mainForm =  document.querySelector("form")
const userInput = document.getElementById("nlp_request")
const chat = document.getElementById("chat")

const addMsgToChat = function(text,cls){

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
    console.log(nlpMsg)
    addMsgToChat(nlpMsg,"chatResponse")
})

const createChart = function(){
    labels = ["BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK","BLACK",]

    var ctx = document.getElementById('chat').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        }
    });
}

console.log("a")
//createChart()