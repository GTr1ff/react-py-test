import type { AppRoute } from "../../../vite-plugins/extract-routes";

declare module "*/routes.generated.json" {
  const routes: AppRoute[];
  export default routes;
}
