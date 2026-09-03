
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { ShoppingListItem, type ShoppingListItemJson } from "./model";
import { shoppingListItemSchema } from "./schema";


const ENDPOINT = "/shopping-list-item";
const TABLE = "shopping_list_item";
const PK = "id";

export const shoppingListItemRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: ShoppingListItem): Promise<ShoppingListItem> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, shoppingListItemSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return ShoppingListItem.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => ShoppingListItem.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<ShoppingListItem> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, shoppingListItemSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return ShoppingListItem.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => ShoppingListItem.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<ShoppingListItem>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, shoppingListItemSchema);
      const items = db.getAll(TABLE).map(ShoppingListItem.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => ShoppingListItem.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<ShoppingListItem>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, shoppingListItemSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(ShoppingListItem.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => ShoppingListItem.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<ShoppingListItemJson>,
  ): Promise<ShoppingListItem> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, shoppingListItemSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return ShoppingListItem.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => ShoppingListItem.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, shoppingListItemSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
