export async function getProductsByFilter(page = 1, Filter = "") {
  const response = await fetch(
    `/paginate/${page}/${encodeURIComponent(Filter)}`
  );
  if (!reponse.ok) {
    throw new Error("query error");
  }
  return await response.json();
}
