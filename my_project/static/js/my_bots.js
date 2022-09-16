var myBot
// old search function lmao
function searchFunction(){
    var input = document.getElementById("myInput").value;
    var count = Object.keys(Bots).length;


    // remove all results prio
    var element = document.getElementById("botContainer");
    element.parentNode.removeChild(element);

    console.log(Bots)

    // loop over every bot
    for (let i = 0; i < count; i++) {
        if (Bots[i]["name"] == input) {
            var myBot = Bots[i]["name"]
            var myBotImage = Bots[i]["image"]
        }
    }
    if (!myBot) {
        var divNone = document.createElement("div");
        var text = document.createTextNode("Nothing found");
        divNone.appendChild(text);
        document.getElementById("modal-body").appendChild(divNone)
    } else {
        var divBot = document.createElement("div");
        var imgDiv = document.createElement("div");
        var img = document.createElement("img");
        var cardBodyDiv = document.createElement("div");
        var nameTextH1 = document.createElement("h1");
        var nameText = document.createTextNode(myBot);
        var button = document.createElement("button");

        // create bot card element
        divBot.classList.add("card");

        imgDiv.classList.add("image-container");
        img.classList.add("image");
        img.setAttribute("src", myBotImage)

        cardBodyDiv.classList.add("card-body");
        nameTextH1.classList.add("name");
        nameTextH1.appendChild(nameText);
        // button.classList.add("btn btn-success");

        imgDiv.appendChild(img);
        divBot.appendChild(imgDiv);
        cardBodyDiv.appendChild(nameTextH1,button);
        divBot.appendChild(cardBodyDiv);

        document.getElementById("modal-body").appendChild(divBot);
    }
}

// toggle visibility
function btterSearchFunction() {
    var input = document.getElementById("myInput").value;
    var botName = "Sportsbot #" + input;
    document.getElementById(botName).style.display = "block";
}

// add button on bot => create that div in the middle part
function addFunction(clicked_id) {

    var selectedBotId = clicked_id - 1;
    // var input = document.getElementById("myInput").value;
    // var addBtn = document.getElementById(clicked_id + 1);
    var myBotImage = Bots[selectedBotId]["image"];

    var divBotX = document.createElement("div");
    var imgDivX = document.createElement("div");
    var imgX = document.createElement("img");
    var cardBodyDivX = document.createElement("div");
    var nameTextH1X = document.createElement("h1");
    var nameTextX = document.createTextNode("Sportsbot #" + selectedBotId);
    var button = document.createElement("button");

    // create bot card element
    divBotX.classList.add("card2");
    divBotX.setAttribute('id','card2')
    imgDivX.classList.add("image-container");
    imgX.classList.add("image");
    imgX.setAttribute("src", myBotImage)
    cardBodyDivX.classList.add("card-body");
    nameTextH1X.classList.add("name");
    nameTextH1X.appendChild(nameTextX);
    button.classList.add("btn", "btn-alert");
    imgDivX.appendChild(imgX);
    divBotX.appendChild(imgDivX);
    cardBodyDivX.appendChild(nameTextH1X);
    cardBodyDivX.appendChild(button);
    divBotX.appendChild(cardBodyDivX);

    document.getElementById("middleBotContainer").appendChild(divBotX);
}


function sendSelectedData() {
    const selectedBotsName = [];
    const container = document.querySelector("#middleBotContainer");
    let selectedBots = container.querySelectorAll("div.card-body > h1")[0].innerText; // only first one rn... need to find a way to find all!!

    selectedBotsName.push(selectedBots)

    console.log(selectedBots)
    console.log(selectedBotsName);

    const request = new XMLHttpRequest();
    request.open('POST', `/my_bots/${JSON.stringify(selectedBotsName)}`);
    request.send();
}
