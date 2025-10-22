export function pagination_interface_render(data) {
  document.getElementById("prev-btn").disabled = data.currentPage == 1;
  document.getElementById("next-btn").disabled = !data.has_next;
  document.getElementById(
    "page-info"
  ).textContent = `Page ${data.current_page} of ${data.total_pages}`;
}
