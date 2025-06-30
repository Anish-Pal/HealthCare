let cross = document.querySelector("#crossimg");
let menu = document.querySelector("#menuimg");
let getMenu = document.querySelector("#sidemenu");

function closeMenu() {
    getMenu.style.right = "-400px";
}

function openMenu() {
    getMenu.style.right = "0";
}

cross.addEventListener("click", closeMenu);
menu.addEventListener("click", openMenu);


function toggleChat() {
  const popup = document.getElementById('chat-popup');
  if (popup.style.display === 'none') {
  popup.style.display = 'flex';
} else {
  popup.style.display = 'none';
}
}

function appendMessage(sender,Text){
    const messages = document.getElementById('chat-messages');
    const messagediv = document.createElement('div');
    messagediv.textContent = `${sender}: ${Text}`;
    messagediv.className = sender === 'You' ? 'user' : 'ai';
    messages.appendChild(messagediv);
    messages.scrollTop = messages.scrollHeight;
    return messagediv;
}

document.getElementById('send-message').addEventListener('click',async()=>{
    const userInput = document.getElementById('chat-input').value;
    appendMessage('You',userInput);
    document.getElementById('chat-input').value = '';
     const aiPlaceholder = appendMessage('AI', 'Typing...');

    try{
      const response = await fetch('/chatbot/',{
        method:"POST",
        headers:{
          'content-type': 'application/json'
        },
        body: JSON.stringify({message: userInput})
      });
      const data = await response.json();

      aiPlaceholder.textContent = `AI: ${data.reply}`;
    }catch(error){
      console.error('Error:', error);
      appendMessage('Ai', 'Sorry, something went wrong.');
    }
});