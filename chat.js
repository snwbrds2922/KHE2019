	document.getElementsByClassName("live-chat-accord")[0].addEventListener("click", function () {
		this.classList.toggle("active-live-chat");
		const panel = this.nextElementSibling;
		panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
	});