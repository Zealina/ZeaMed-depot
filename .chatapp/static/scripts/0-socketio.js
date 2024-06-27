const socket = io();
socket.on('connect', function () {
  console.log("Hamilton is Awesome!");
});
