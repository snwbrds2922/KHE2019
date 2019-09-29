let websocket;
let v;
let clients = 0;

chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 255, 255] });
chrome.browserAction.setBadgeText({text: String(clients)});

chrome.runtime.onConnect.addListener(function(port) {
  console.assert(port.name == "knockknock");
  if (port.name == "videoID") {
	port.onMessage.addListener(function(msg) {
		if (msg.vid) {
			port.postMessage({goit: msg.vid});
			v = msg.vid;
			createWebSocketConnection();
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
				clients = messData;
				chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 255, 255] });
				chrome.browserAction.setBadgeText({text: String(clients)});
			break;
			case 'MSG':
				// write the data to chat
			break;
		}

    };

    websocket.onclose = function() {
        websocket = undefined;
    };
}

//Close the websocket connection
function closeWebSocketConnection(username) {
    if (websocket != null || websocket != undefined) {
        websocket.close();
        websocket = undefined;
    }
}