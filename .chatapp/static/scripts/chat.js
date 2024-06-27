const socket = io({autoConnect: false});

document.getElementById("join-btn").addEventListener("click", function() {
  let username = document.getElementById("username").value;

  socket.connect();
  

  socket.on("connect", function () {
    socket.emit("user_join", username);
  });
  
  document.getElementById("chat-container").style.display = "block";
  document.getElementById("login-container").style.display = "none";

 
});

document.getElementById("send-btn").addEventListener("click", function() {
  let msg = document.getElementById("message-input").value;
  socket.emit("new_message", msg);
  document.getElementById("message-input").value = "";
});

socket.on("chat", function (data) {
  console.log(data);
  let ul = document.getElementById("chat-msg");
  let li = document.createElement("li");
  li.appendChild(document.createTextNode(data["message"]));
  ul.appendChild(li);
});
