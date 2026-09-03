
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { Ingredient, type IngredientJson } from "./model";
import { ingredientSchema } from "./schema";


const ENDPOINT = "/ingredient";
const TABLE = "ingredient";
const PK = "id";

export const ingredientRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: Ingredient): Promise<Ingredient> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, ingredientSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return Ingredient.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => Ingredient.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<Ingredient> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, ingredientSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return Ingredient.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => Ingredient.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<Ingredient>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, ingredientSchema);
      const items = db.getAll(TABLE).map(Ingredient.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => Ingredient.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<Ingredient>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, ingredientSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(Ingredient.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => Ingredient.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<IngredientJson>,
  ): Promise<Ingredient> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, ingredientSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return Ingredient.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => Ingredient.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, ingredientSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
