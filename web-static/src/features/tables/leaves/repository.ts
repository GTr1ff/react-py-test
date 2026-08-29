
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { Leaf, type LeafJson } from "./model";
import { leavesSchema } from "./schema";


const ENDPOINT = "/leaves";
const TABLE = "leaves";
const PK = "leaveId";

export const leavesRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: Leaf): Promise<Leaf> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, leavesSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return Leaf.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => Leaf.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<Leaf> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, leavesSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return Leaf.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => Leaf.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<Leaf>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, leavesSchema);
      const items = db.getAll(TABLE).map(Leaf.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => Leaf.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<Leaf>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, leavesSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(Leaf.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => Leaf.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<LeafJson>,
  ): Promise<Leaf> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, leavesSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return Leaf.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => Leaf.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, leavesSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
