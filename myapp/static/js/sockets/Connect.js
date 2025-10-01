document.querySelectorAll('.join-auction').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const roomToken = e.target.dataset.roomToken;
    socket.emit('join_room', roomToken);

    window.location.href = `/auction/${productId}?room=${roomToken}`;
  });
});