export async function getProductsByFilter(page = 1, Filter = "") {
  const endpoint = Filter
    ? `/paginate/${page}/${encodeURIComponent(Filter)}`
    : `/paginate/${page}`;

  const response = await fetch(endpoint);

  if (!response.ok) {
    throw new Error("query error");
  }

  return await response.json();
}
