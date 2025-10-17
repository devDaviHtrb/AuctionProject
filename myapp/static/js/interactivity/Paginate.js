import { getProductsByFilter } from "../api/GetProductsByFilter.js";
import { renderProducts } from "../ui/RenderProducts.js";
import { pagination_interface_render } from "../ui/Pagination.js";

export async function loadProducts(page = 1, Filter = "") {
  try {
    const data = await getProductsByFilter(page, Filter);
    renderProducts(data);
    pagination_interface_render(data, data.current_page);
    return data.current_page;
  } catch (err) {
    console.error(err);
    return page;
  }
}
