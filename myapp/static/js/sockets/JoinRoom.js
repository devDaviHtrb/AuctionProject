export function joinRoom(e) {
  e.preventDefault();
  const room = e.target.dataset.roomToken;
  socket.emit("join_room", room);
  window.location.href = `/auction/${room}`;
}
