document.addEventListener("DOMContentLoaded", function(event) {
	document.getElementsByClassName("live-chat-accord")[0].addEventListener("click", function() {
		this.classList.toggle("active-live-chat");
		var panel = this.nextElementSibling;
		if (panel.style.display === "block") {
			panel.style.display = "none";
		} else {
			panel.style.display = "block";
		}
	});
});
