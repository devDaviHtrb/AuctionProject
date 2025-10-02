import { getProductsByFilter } from "../api/GetProductsByFilter";
import { renderProducts } from "../ui/RenderProducts";
import { pagination_interface_render } from "../ui/Pagination";
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
