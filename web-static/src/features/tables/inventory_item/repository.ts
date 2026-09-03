
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { InventoryItem, type InventoryItemJson } from "./model";
import { inventoryItemSchema } from "./schema";


const ENDPOINT = "/inventory-item";
const TABLE = "inventory_item";
const PK = "id";

export const inventoryItemRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: InventoryItem): Promise<InventoryItem> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, inventoryItemSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return InventoryItem.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => InventoryItem.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<InventoryItem> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, inventoryItemSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return InventoryItem.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => InventoryItem.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<InventoryItem>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, inventoryItemSchema);
      const items = db.getAll(TABLE).map(InventoryItem.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => InventoryItem.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<InventoryItem>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, inventoryItemSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(InventoryItem.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => InventoryItem.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<InventoryItemJson>,
  ): Promise<InventoryItem> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, inventoryItemSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return InventoryItem.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => InventoryItem.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, inventoryItemSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
