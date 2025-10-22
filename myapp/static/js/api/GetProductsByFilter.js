export async function getProductsByFilter(page = 1, Filter = "") {
  const endpoint = Filter
    ? `/paginate/auctions/${page}/${encodeURIComponent(Filter)}`
    : `/paginate/auctions/${page}`;

  const response = await fetch(endpoint);

  if (!response.ok) {
    throw new Error("query error");
  }

  return await response.json();
}
