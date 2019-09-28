const url = new URL(window.location);
const params = new URLSearchParams(url.search);
const v = params.get('v');
const chat = document.createElement('div');
chat.style.cssText = 'position:fixed;bottom:0;right:0;z-index:9999;';
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