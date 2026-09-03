
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { RecipeIngredient, type RecipeIngredientJson } from "./model";
import { recipeIngredientSchema } from "./schema";


const ENDPOINT = "/recipe-ingredient";
const TABLE = "recipe_ingredient";
const PK = "recipeId";

export const recipeIngredientRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: RecipeIngredient): Promise<RecipeIngredient> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeIngredientSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return RecipeIngredient.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => RecipeIngredient.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<RecipeIngredient> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeIngredientSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return RecipeIngredient.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => RecipeIngredient.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<RecipeIngredient>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeIngredientSchema);
      const items = db.getAll(TABLE).map(RecipeIngredient.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => RecipeIngredient.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<RecipeIngredient>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeIngredientSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(RecipeIngredient.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => RecipeIngredient.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<RecipeIngredientJson>,
  ): Promise<RecipeIngredient> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeIngredientSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return RecipeIngredient.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => RecipeIngredient.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, recipeIngredientSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
