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

    //console.log(chat.style.height)

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
    
    //console.log(await response)
   // console.log(response.nlpResponse.length)

    for(let i=0; i<response.nlpResponse.length; i++){
        let nlpMsg = response.nlpResponse[i]
        //console.log(nlpMsg)

        if (nlpMsg.Action == "List")
        {
            addMsgToChat(nlpMsg.Response,"chatResponse")
        }
        else if (nlpMsg.Action == "Graph")
        {   
            console.log(nlpMsg.Response)
            createChart(nlpMsg.Response)
        }
        //createChart([1,2,2,3,4,5,6,7,8],["a","a","a","a","a","a","a","a"])
        //addMsgToChat(nlpMsg,"chatResponse")
    
        chat.scrollTo({
            top: chat.scrollHeight,
            behavior: 'smooth'
          });
    }

})

function stringToColorRGBA(str,alpha) {
    
    color = {
        'LAS AMERICAS':`rgba(255, 206, 86, ${alpha}`,
        'PUERTO PLATA': `rgba(54, 162, 235, ${alpha})`,
        'PUNTA CANA':`rgba(255, 99, 132, ${alpha})`,
        'LA ROMANA':`rgba(75, 192, 192, ${alpha})`,
        'CIBAO': `rgba(153, 102, 255, ${alpha})`,
        'HERRERA': `rgba(255, 159, 64, ${alpha})`,
        'LA ISABELA': `rgba(219, 252, 3, ${alpha})`,
        'EL CATEY, SAMANA': `rgba(177, 3, 252, ${alpha})`,
        'MARÍA MONTEZ' : `rgba(3, 252, 206, ${alpha})`
    }
    return color[str]
}


const generateColor = function(labels,alpha){

    colors = [stringToColorRGBA(labels,alpha)]
    console.log(colors)
    return colors;
}

const generateData = function(data){
    
    let datas = []
    let year = []
    for (let key in data) {

        year = []
        value = []

        data[key].forEach(element => {
            year.push(element[1])
            value.push(element[0])
        });

        datas.push({
            label: key,
            data: value,
            backgroundColor: generateColor(key,0.2),
            borderColor: generateColor(key,1),
            borderWidth: 1
        })
      }
      return [datas,year]
}

const createChart = function(dataArray){

    let data = generateData(dataArray)
    console.log("generated data IS")
    console.log(data)
    let canvas = document.createElement("canvas")
    canvas.style.width = "100%"

    chat.appendChild(canvas)
    //let labels = ["BLACK","BLACK","BLACK","BLACK"]

    var ctx = canvas.getContext('2d');
    console.log(ctx)
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data[1],
            datasets: data[0]
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

//createChart([1,2,3,4,5,6,7,8],["a","a","a","a","a","a","a","a"])