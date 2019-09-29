let websocket;
let v;
let clients = 0;

chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 255, 255] });
chrome.browserAction.setBadgeText({text: String(clients)});

chrome.runtime.onConnect.addListener(function(port) {
  if (port.name == "videoID") {
	port.onMessage.addListener(function(msg) {
		if (msg.vid) {
			v = msg.vid;
			createWebSocketConnection();
		}
		if (msg.msgval) {
			sendChatMessage(String(msg.msgval).replace(":", ""));
		}
	});
  }
});

function createWebSocketConnection() {
    if('WebSocket' in window){
		connect('ws://157.245.135.82:8766');
    }
}

function connect(host) {
    if (websocket === undefined) {
        websocket = new WebSocket(host);
    }

    websocket.onopen = function() {
		// in the beginning send the videoID to the server
		websocket.send("CONNECT:" + v);
    };

    websocket.onmessage = function (event) {
		let messType = event.data.split(':')[0];
		let messData = event.data.split(':')[1];
		switch (messType) {
			case 'UPDATE':
				chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
					chrome.tabs.sendMessage(tabs[0].id, {update: messData >= clients ? "joined" : "left"});
				});
				clients = messData;
				chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 255, 255] });
				chrome.browserAction.setBadgeText({text: String(clients)});
			break;
			case 'MESSAGE':
				// write the data to chat
				chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
					chrome.tabs.sendMessage(tabs[0].id, {message: "[Client " + messData + "]" + event.data.split(':')[2]});
				});
			break;
		}

    };

    websocket.onclose = function() {
        websocket = undefined;
    };
}

function sendChatMessage(msg) {
	if (websocket != null || websocket != undefined) {
		websocket.send("MESSAGE:" + msg);
	}
}

//Close the websocket connection
function closeWebSocketConnection(username) {
    if (websocket != null || websocket != undefined) {
        websocket.close();
        websocket = undefined;
    }
}

let username = 'flarelation';
const url = 'https://core.blockstack.org/v1/names/flarelation.id.blockstack';
let token = undefined;

fetch(url)
.then(response => response.json())
.then((data) => {
  token = data.address;
  
  window.localStorage.setItem("token", token);
})
.catch(err => { throw err });