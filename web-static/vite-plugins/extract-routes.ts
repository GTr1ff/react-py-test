/**
 * Vite plugin that scrapes <Route> declarations from a source file and
 * writes the resulting object array to a JSON file.
 */
import type { Plugin } from "vite";
import fs from "node:fs";
import path from "node:path";

export interface AppRoute {
  id: string;
  name: string;
  path: string;
}

export interface ExtractRoutesOptions {
  sourceFile: string;
  outputFile: string;
}

const ROUTE_REGEX =
  /<Route\s+[^>]*?path=["']([^"']+)["'][^>]*?element=\{\s*<\s*([A-Za-z_][\w]*)/g;

const ALIAS_ELEMENTS = new Set(["Navigate", "Redirect"]);

const stripComments = (source: string): string =>
  source
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, "")
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/(^|[^:'"`])\/\/.*$/gm, "$1");

const slugify = (value: string): string =>
  value
    .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase() || "route";

const humanize = (value: string): string =>
  value
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .replace(/([A-Z]+)([A-Z][a-z])/g, "$1 $2")
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase()) || "Screen";

const extractAppRoutes = (source: string): AppRoute[] => {
  const cleanedRoute = stripComments(source);
  const routes: AppRoute[] = [];
  const seenRoutes = new Map<string, number>();

  ROUTE_REGEX.lastIndex = 0;
  let match: RegExpExecArray | null;
  while ((match = ROUTE_REGEX.exec(cleanedRoute)) !== null) {
    const [, routePath, name] = match;
    // exclude dynamic routes and catch-all routes since they can't be linked to directly
    if (/[:*]/.test(routePath)) continue;
    // exclude redirect aliases (e.g. <Route element={<Navigate to=... />} />)
    if (ALIAS_ELEMENTS.has(name)) continue;
    const base = slugify(name);
    const count = seenRoutes.get(base) ?? 0;
    const id = count === 0 ? base : `${base}-${count}`;
    seenRoutes.set(base, count + 1);
    routes.push({ id, name: humanize(name), path: routePath });
  }

  return routes;
};

export const extractRoutesPlugin = (options: ExtractRoutesOptions): Plugin => {
  let sourceFile = "";
  let outputFile = "";

  const generate = () => {
    const source = fs.readFileSync(sourceFile, "utf-8");
    const routes = extractAppRoutes(source);
    const next = `${JSON.stringify(routes, null, 2)}\n`;

    fs.mkdirSync(path.dirname(outputFile), { recursive: true });

    let prev = "";
    try {
      prev = fs.readFileSync(outputFile, "utf-8");
    } catch {
      // file doesn't exist yet
    }
    if (prev !== next) {
      fs.writeFileSync(outputFile, next);
    }
  };

  return {
    name: "vite-plugin-extract-routes",
    enforce: "pre",
    configResolved(config) {
      sourceFile = path.resolve(config.root, options.sourceFile);
      outputFile = path.resolve(config.root, options.outputFile);
      generate();
    },
    buildStart() {
      this.addWatchFile(sourceFile);
      generate();
    },
    handleHotUpdate({ file, server }) {
      if (file !== sourceFile) return;
      generate();
      const mod = server.moduleGraph.getModuleById(outputFile);
      return mod ? [mod] : [];
    },
  };
};
