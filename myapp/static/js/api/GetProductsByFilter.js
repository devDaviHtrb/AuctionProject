export async function getProductsByFilter(page = 1, Filter = "") {
  const response = await fetch(
    `/paginate?page=${page}&filter=${encodeURIComponent(Filter)}`
  );
  if (!reponse.ok) {
    throw new Error("query error");
  }
  return await response.json();
}
