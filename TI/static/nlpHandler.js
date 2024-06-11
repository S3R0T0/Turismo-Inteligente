const mainForm =  document.querySelector("form")
const userInput = document.getElementById("nlp_request")
const chat = document.getElementById("chat")


document.addEventListener("click",()=>{
    buttons= document.querySelectorAll("#menu")

    buttons.forEach(element => {
        if (element.getAttribute("save")=="false"){
            element.remove()
        }else{
            element.setAttribute("save", false);
        }
    });
})

const addMsgToChat = function(text,cls){

    let newMsg = document.createElement("h1")
    newMsg.classList.add(cls,"chatMsg")
    newMsg.textContent = text
    chat.appendChild(newMsg)

    console.log(chat.style.height)

    newMsg.addEventListener("click",(e)=>{
        menu = document.createElement("h1")
        menu.setAttribute("id", "menu");
        menu.setAttribute("save", true);

        btn1 = document.createElement("button")
        btn1.classList.add("cntButton")
        btn1.textContent = "Copy"
        btn1.style.fontSize = '10px'

        btn2 = document.createElement("button")
        btn2.classList.add("cntButton")
        btn2.textContent = "Delete"
        btn2.style.fontSize = '10px'

        menu.style.left = e.x + 'px';
        menu.style.top = e.y + 'px';

        document.body.appendChild(menu)
        menu.appendChild(btn1)
        menu.appendChild(btn2)

        btn1.addEventListener("click",()=>navigator.clipboard.writeText(text))
        btn2.addEventListener("click",()=>newMsg.remove())

    })
}

mainForm.addEventListener("submit",async (event)=>{
    event.preventDefault()

    if(userInput.value == "") return

    addMsgToChat(userInput.value,"chatRequest")

    let request = await fetch(mainForm.action+`?nlp_request=${userInput.value}`)
    let response = await request.json()
    let nlpMsg = response.nlpResponse
    console.log(nlpMsg)
    createChart([1,2,2,3,4,5,6,7,8],["a","a","a","a","a","a","a","a"])
    //addMsgToChat(nlpMsg,"chatResponse")

    chat.scrollTo({
        top: chat.scrollHeight,
        behavior: 'smooth'
      });


})

const createChart = function(dataArray,labels){

    let canvas = document.createElement("canvas")
    canvas.style.width = "100%"

    chat.appendChild(canvas)

    //let labels = ["BLACK","BLACK","BLACK","BLACK"]

    var ctx = canvas.getContext('2d');
    console.log(ctx)
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: dataArray,
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
        },
        
        options: {
            responsive: false,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

createChart([1,2,3,4,5,6,7,8],["a","a","a","a","a","a","a","a"])