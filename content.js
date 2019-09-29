window.addEventListener('yt-navigate-finish', finishNav);

function finishNav() {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);
    const v = params.get('v');
	if (v) {
		const chat = document.createElement('div');
		chat.setAttribute('class', 'this-is-parent-live-chat');
		chat.innerHTML = `
		<div class="live-chat">
		  <button class="live-chat-accord">Current Users 2</button>
		  <div class="panel-live-chat">
			<input class="live-sub-chat" type="text">
			<form class="livechat-sub">
			  <input class="live-sub-mess" type="text" placeholder="Message">
			  <input class="live-sub-button" type="submit" value="Submit">
			</form>
		  </div>
		</div>
		`;
		document.body.appendChild(chat);
		
		chat.querySelector('.live-chat-accord').addEventListener('click', function () {
			this.classList.toggle("active-live-chat");
			const panel = this.nextElementSibling;
			panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
		});
		
		var port = chrome.runtime.connect({name: "videoID"});
		port.postMessage({vid: v});
		port.onMessage.addListener(function(msg) {
		  if (msg.goit == v) {
			  alert(v);
		  }
		  
		});
	} else if(document.querySelector(".this-is-parent-live-chat")) {
		document.querySelector(".this-is-parent-live-chat").remove();
	}
}

finishNav();

