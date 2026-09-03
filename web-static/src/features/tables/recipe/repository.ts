
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { Recipe, type RecipeJson } from "./model";
import { recipeSchema } from "./schema";


const ENDPOINT = "/recipe";
const TABLE = "recipe";
const PK = "id";

export const recipeRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: Recipe): Promise<Recipe> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return Recipe.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => Recipe.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<Recipe> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return Recipe.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => Recipe.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<Recipe>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeSchema);
      const items = db.getAll(TABLE).map(Recipe.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => Recipe.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<Recipe>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(Recipe.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => Recipe.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<RecipeJson>,
  ): Promise<Recipe> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return Recipe.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => Recipe.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
